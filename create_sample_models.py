#!/usr/bin/env python3
"""
Script to create sample ML model and encoders for MindMetric AI
This creates realistic model files for demonstration purposes
"""

import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd

def create_sample_data():
    """Create sample training data that mimics psychological assessment responses"""
    np.random.seed(42)  # For reproducible results
    
    # Sample responses for 1000 users
    n_samples = 1000
    
    # Generate personality/stress responses (Q1-Q10)
    data = {}
    for i in range(1, 11):
        data[f'q{i}'] = np.random.choice(['A', 'B', 'C', 'D', 'E'], n_samples)
    
    # Generate stress scores (0-10)
    data['stress_score'] = np.random.uniform(0, 10, n_samples)
    
    # Generate derived features
    data['high_stress_count'] = np.random.randint(0, 6, n_samples)
    data['low_stress_count'] = np.random.randint(0, 6, n_samples)
    
    # Create target labels (content types)
    content_types = ['Meditation', 'Nature Sounds', 'Relaxing Music', 'Guided Breathing', 'Professional Therapy', 'Podcasts']
    
    # Create some logical patterns in the data
    targets = []
    for i in range(n_samples):
        stress_score = data['stress_score'][i]
        high_stress = data['high_stress_count'][i]
        
        if stress_score < 2:
            targets.append('Meditation')
        elif stress_score < 4:
            targets.append('Nature Sounds')
        elif stress_score < 6:
            targets.append('Relaxing Music')
        elif stress_score < 8:
            targets.append('Guided Breathing')
        elif high_stress > 3:
            targets.append('Professional Therapy')
        else:
            targets.append('Podcasts')
    
    data['target'] = targets
    
    return pd.DataFrame(data)

def create_encoders(df):
    """Create label encoders for categorical variables"""
    encoders = {}
    
    # Create encoders for Q1-Q10 responses
    for i in range(1, 11):
        encoder = LabelEncoder()
        encoder.fit(['A', 'B', 'C', 'D', 'E'])  # Fit with all possible values
        encoders[f'q{i}'] = encoder
    
    return encoders

def prepare_features(df, encoders):
    """Prepare feature matrix for training"""
    features = []
    
    # Encode Q1-Q10 responses
    for i in range(1, 11):
        encoded = encoders[f'q{i}'].transform(df[f'q{i}'])
        features.append(encoded)
    
    # Add stress score and derived features
    features.append(df['stress_score'].values)
    features.append(df['high_stress_count'].values)
    features.append(df['low_stress_count'].values)
    
    return np.column_stack(features)

def create_and_save_model():
    """Create and save the ML model and encoders"""
    print("Creating sample training data...")
    df = create_sample_data()
    
    print("Creating label encoders...")
    encoders = create_encoders(df)
    
    print("Preparing features...")
    X = prepare_features(df, encoders)
    y = df['target'].values
    
    print("Training model...")
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Check accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    print("Saving model...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Saving encoders...")
    with open('encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)
    
    print("✓ Model and encoders created successfully!")
    print("Files created:")
    print("  - model.pkl (RandomForest classifier)")
    print("  - encoders.pkl (Label encoders for categorical variables)")
    
    # Test the saved model
    print("\nTesting saved model...")
    test_model()

def test_model():
    """Test the saved model with sample data"""
    # Load model and encoders
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    
    # Test with sample responses
    test_responses = {
        'q1': 'A', 'q2': 'B', 'q3': 'C', 'q4': 'D', 'q5': 'E',
        'q6': 'A', 'q7': 'B', 'q8': 'C', 'q9': 'D', 'q10': 'E'
    }
    test_stress_score = 5.5
    
    # Prepare test features
    features = []
    for i in range(1, 11):
        encoded = encoders[f'q{i}'].transform([test_responses[f'q{i}']])[0]
        features.append(encoded)
    
    features.append(test_stress_score)
    features.append(2)  # high_stress_count
    features.append(3)  # low_stress_count
    
    # Make prediction
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0]
    
    print(f"Test prediction: {prediction}")
    print("Prediction probabilities:")
    for i, class_name in enumerate(model.classes_):
        print(f"  {class_name}: {probabilities[i]:.3f}")

if __name__ == "__main__":
    create_and_save_model()