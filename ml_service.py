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
    """Enhanced fallback prediction based on stress score and research"""
    # More sophisticated prediction based on psychological research
    if stress_score <= 2:
        # Low stress - maintenance and prevention
        options = ["Meditation", "Nature Sounds", "Music"]
        return options[int(stress_score) % len(options)]
    elif stress_score <= 4:
        # Mild stress - gentle interventions
        options = ["Guided Breathing", "Music", "Meditation"]
        return options[int(stress_score * 2) % len(options)]
    elif stress_score <= 6:
        # Moderate stress - active interventions
        options = ["Guided Breathing", "Podcasts", "Music"]
        return options[int(stress_score) % len(options)]
    elif stress_score <= 8:
        # High stress - structured interventions
        options = ["Professional Therapy", "Guided Breathing", "Podcasts"]
        return options[int(stress_score) % len(options)]
    else:
        # Very high stress - immediate professional support
        return "Professional Therapy"

def get_prediction_confidence(stress_score):
    """Calculate confidence level for prediction"""
    if stress_score <= 3 or stress_score >= 8:
        return 0.85  # High confidence for extreme scores
    else:
        return 0.75  # Medium confidence for middle range

def get_detailed_recommendations(prediction, stress_score):
    """Get detailed recommendations based on prediction"""
    recommendations = {
        "Meditation": {
            "description": "Mindfulness practices to reduce stress and improve mental clarity",
            "specific_techniques": ["Guided meditation", "Body scan", "Breathing meditation", "Walking meditation"],
            "duration": "10-20 minutes daily",
            "apps": ["Headspace", "Calm", "Insight Timer"]
        },
        "Music": {
            "description": "Therapeutic music to regulate emotions and reduce anxiety",
            "specific_techniques": ["Classical music", "Nature sounds with music", "Binaural beats", "Instrumental music"],
            "duration": "30-60 minutes as needed",
            "apps": ["Spotify (wellness playlists)", "YouTube Music", "Apple Music"]
        },
        "Nature Sounds": {
            "description": "Natural audio environments for relaxation and stress relief",
            "specific_techniques": ["Rain sounds", "Ocean waves", "Forest sounds", "White noise"],
            "duration": "Background listening or 15-30 minutes",
            "apps": ["Rain Rain", "Noisli", "Brain.fm"]
        },
        "Guided Breathing": {
            "description": "Structured breathing exercises for immediate stress relief",
            "specific_techniques": ["4-7-8 breathing", "Box breathing", "Progressive relaxation", "Coherent breathing"],
            "duration": "5-15 minutes per session",
            "apps": ["Breathe", "Pranayama", "Breathwrk"]
        },
        "Podcasts": {
            "description": "Educational content for mental health awareness and coping strategies",
            "specific_techniques": ["Psychology podcasts", "Self-help content", "Meditation guides", "Therapy sessions"],
            "duration": "20-60 minutes per episode",
            "apps": ["Spotify", "Apple Podcasts", "Google Podcasts"]
        },
        "Professional Therapy": {
            "description": "Professional psychological support for comprehensive mental health care",
            "specific_techniques": ["Cognitive Behavioral Therapy", "Mindfulness-based therapy", "Stress management", "Individual counseling"],
            "duration": "45-60 minutes per session",
            "providers": ["Licensed psychologists", "Mental health counselors", "Psychiatrists"]
        }
    }
    
    return recommendations.get(prediction, {
        "description": "Personalized mental wellness approach",
        "specific_techniques": ["Consult with mental health professional"],
        "duration": "As recommended by professional",
        "providers": ["Mental health professionals"]
    })
