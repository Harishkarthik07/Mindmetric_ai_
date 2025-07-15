import pickle
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import logging

def load_model_and_encoders():
    """Load the trained ML model and encoders"""
    try:
        # Load model
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Load encoders
        with open('encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        
        return model, encoders
    except FileNotFoundError as e:
        logging.error(f"Model files not found: {e}")
        # Return None if files don't exist - we'll use a fallback prediction
        return None, None
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None, None

def calculate_stress_score(stress_responses):
    """Calculate stress score from 0-10 based on stress level responses"""
    if not stress_responses:
        return 0.0
    
    # Convert 1-3 scale to 0-10 scale
    # 1 (Low) -> 0-2, 2 (Medium) -> 3-6, 3 (High) -> 7-10
    total_score = sum(stress_responses)
    max_possible = len(stress_responses) * 3
    normalized_score = (total_score / max_possible) * 10
    
    return round(normalized_score, 2)

def predict_content_type(responses, stress_score):
    """Predict ideal content type based on user responses"""
    model, encoders = load_model_and_encoders()
    
    if model is None or encoders is None:
        # Fallback prediction based on stress score
        return get_fallback_prediction(stress_score)
    
    try:
        # Prepare features for prediction
        features = prepare_features(responses, stress_score, encoders)
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        return prediction
    except Exception as e:
        logging.error(f"Error making prediction: {e}")
        return get_fallback_prediction(stress_score)

def prepare_features(responses, stress_score, encoders):
    """Convert responses to features for ML model"""
    features = []
    
    # Add personality/stress responses (Q1-Q10)
    for i in range(1, 11):
        response = responses.get(f'q{i}', 'A')  # Default to 'A' if missing
        if f'q{i}' in encoders:
            encoded = encoders[f'q{i}'].transform([response])[0]
            features.append(encoded)
        else:
            # Simple encoding if encoder not available
            features.append(ord(response) - ord('A'))
    
    # Add stress score
    features.append(stress_score)
    
    # Add derived features
    features.append(len([r for r in responses.values() if r in ['D', 'E']]))  # High stress indicators
    features.append(len([r for r in responses.values() if r in ['A', 'B']]))  # Low stress indicators
    
    return features

def get_fallback_prediction(stress_score):
    """Fallback prediction when model is not available"""
    content_types = {
        (0, 2): "Meditation",
        (2, 4): "Nature Sounds",
        (4, 6): "Relaxing Music",
        (6, 8): "Guided Breathing",
        (8, 10): "Professional Therapy"
    }
    
    for (low, high), content_type in content_types.items():
        if low <= stress_score < high:
            return content_type
    
    return "Meditation"  # Default fallback
