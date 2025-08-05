#!/usr/bin/env python3
"""
Standard Crop Recommendation Model Training Script
Creates the best performing standard model for crop recommendation
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

def create_comprehensive_dataset():
    """Create comprehensive crop recommendation dataset"""
    print("🌾 Creating comprehensive crop recommendation dataset...")
    
    # Define crops
    crops = [
        'apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton',
        'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans',
        'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate',
        'rice', 'watermelon', 'wheat', 'tomato', 'potato', 'onion', 'barley'
    ]
    
    # Generate realistic training data based on agricultural knowledge
    np.random.seed(42)  # For reproducibility
    data = []
    
    # Crop-specific parameter ranges based on agricultural science
    crop_params = {
        'rice': {'N': (80, 120), 'P': (40, 80), 'K': (40, 80), 'temp': (20, 35), 'humidity': (80, 95), 'pH': (5.5, 7.0), 'rainfall': (1200, 2500)},
        'wheat': {'N': (60, 100), 'P': (30, 60), 'K': (30, 60), 'temp': (15, 25), 'humidity': (50, 70), 'pH': (6.0, 7.5), 'rainfall': (400, 800)},
        'maize': {'N': (80, 120), 'P': (40, 80), 'K': (40, 80), 'temp': (20, 30), 'humidity': (60, 80), 'pH': (5.8, 7.2), 'rainfall': (500, 1000)},
        'cotton': {'N': (60, 100), 'P': (30, 60), 'K': (50, 90), 'temp': (21, 32), 'humidity': (50, 80), 'pH': (5.8, 8.0), 'rainfall': (500, 1200)},
        'sugarcane': {'N': (80, 140), 'P': (40, 80), 'K': (80, 120), 'temp': (21, 27), 'humidity': (75, 85), 'pH': (6.0, 7.5), 'rainfall': (1000, 1500)},
        'coffee': {'N': (50, 80), 'P': (30, 50), 'K': (60, 100), 'temp': (15, 25), 'humidity': (70, 85), 'pH': (6.0, 7.0), 'rainfall': (1500, 2500)},
        'apple': {'N': (40, 80), 'P': (20, 40), 'K': (40, 80), 'temp': (15, 25), 'humidity': (50, 70), 'pH': (5.5, 7.0), 'rainfall': (1000, 1200)},
        'mango': {'N': (50, 90), 'P': (30, 60), 'K': (50, 90), 'temp': (24, 32), 'humidity': (50, 75), 'pH': (5.5, 7.5), 'rainfall': (750, 2500)},
        'grapes': {'N': (40, 80), 'P': (30, 60), 'K': (80, 120), 'temp': (15, 25), 'humidity': (50, 70), 'pH': (6.0, 7.5), 'rainfall': (500, 800)},
        'banana': {'N': (100, 150), 'P': (50, 100), 'K': (200, 300), 'temp': (26, 30), 'humidity': (75, 85), 'pH': (5.5, 7.0), 'rainfall': (1500, 2500)},
        'coconut': {'N': (50, 90), 'P': (30, 60), 'K': (100, 150), 'temp': (27, 32), 'humidity': (70, 85), 'pH': (5.2, 8.0), 'rainfall': (1200, 2000)},
        'chickpea': {'N': (20, 40), 'P': (40, 80), 'K': (20, 40), 'temp': (20, 30), 'humidity': (60, 70), 'pH': (6.2, 7.8), 'rainfall': (400, 650)},
        'kidneybeans': {'N': (20, 40), 'P': (40, 80), 'K': (20, 40), 'temp': (15, 25), 'humidity': (65, 75), 'pH': (6.0, 7.5), 'rainfall': (300, 600)},
        'pigeonpeas': {'N': (20, 40), 'P': (30, 60), 'K': (15, 35), 'temp': (26, 30), 'humidity': (60, 75), 'pH': (6.5, 7.5), 'rainfall': (600, 1000)},
        'mothbeans': {'N': (20, 40), 'P': (40, 80), 'K': (20, 40), 'temp': (27, 32), 'humidity': (50, 65), 'pH': (6.0, 8.0), 'rainfall': (400, 650)},
        'mungbean': {'N': (20, 40), 'P': (40, 80), 'K': (20, 40), 'temp': (25, 35), 'humidity': (60, 75), 'pH': (6.2, 7.2), 'rainfall': (500, 750)},
        'blackgram': {'N': (20, 40), 'P': (40, 80), 'K': (20, 40), 'temp': (25, 35), 'humidity': (60, 70), 'pH': (6.5, 7.5), 'rainfall': (600, 1000)},
        'lentil': {'N': (20, 40), 'P': (40, 80), 'K': (20, 40), 'temp': (18, 30), 'humidity': (60, 70), 'pH': (6.0, 7.5), 'rainfall': (300, 400)},
        'pomegranate': {'N': (40, 80), 'P': (30, 60), 'K': (40, 80), 'temp': (15, 25), 'humidity': (35, 55), 'pH': (5.5, 7.5), 'rainfall': (500, 700)},
        'watermelon': {'N': (80, 120), 'P': (40, 80), 'K': (80, 120), 'temp': (24, 32), 'humidity': (50, 70), 'pH': (6.0, 7.0), 'rainfall': (400, 600)},
        'muskmelon': {'N': (80, 120), 'P': (40, 80), 'K': (80, 120), 'temp': (25, 35), 'humidity': (50, 70), 'pH': (6.5, 7.5), 'rainfall': (400, 600)},
        'orange': {'N': (50, 90), 'P': (30, 60), 'K': (50, 90), 'temp': (15, 30), 'humidity': (55, 75), 'pH': (6.0, 7.5), 'rainfall': (1200, 1800)},
        'papaya': {'N': (60, 100), 'P': (40, 80), 'K': (60, 100), 'temp': (22, 32), 'humidity': (60, 85), 'pH': (5.5, 7.0), 'rainfall': (1000, 2000)},
        'jute': {'N': (60, 100), 'P': (30, 60), 'K': (30, 60), 'temp': (24, 35), 'humidity': (70, 90), 'pH': (6.0, 7.5), 'rainfall': (1200, 1800)},
        'tomato': {'N': (80, 120), 'P': (60, 100), 'K': (100, 150), 'temp': (20, 30), 'humidity': (60, 80), 'pH': (6.0, 7.0), 'rainfall': (600, 1200)},
        'potato': {'N': (80, 120), 'P': (40, 80), 'K': (100, 150), 'temp': (15, 25), 'humidity': (70, 85), 'pH': (5.2, 6.4), 'rainfall': (500, 700)},
        'onion': {'N': (60, 100), 'P': (40, 80), 'K': (80, 120), 'temp': (13, 24), 'humidity': (60, 70), 'pH': (6.0, 7.5), 'rainfall': (600, 1000)},
        'barley': {'N': (50, 90), 'P': (25, 50), 'K': (25, 50), 'temp': (12, 25), 'humidity': (55, 70), 'pH': (6.0, 7.5), 'rainfall': (450, 650)}
    }
    
    # Generate data for each crop
    for crop in crops:
        if crop in crop_params:
            params = crop_params[crop]
        else:
            # Default parameters for crops not specifically defined
            params = {'N': (40, 100), 'P': (30, 80), 'K': (40, 100), 'temp': (20, 30), 'humidity': (60, 80), 'pH': (6.0, 7.5), 'rainfall': (800, 1200)}
        
        # Generate 100 samples per crop for robust training
        for _ in range(100):
            sample = {
                'N': np.random.randint(params['N'][0], params['N'][1] + 1),
                'P': np.random.randint(params['P'][0], params['P'][1] + 1),
                'K': np.random.randint(params['K'][0], params['K'][1] + 1),
                'temperature': np.round(np.random.uniform(params['temp'][0], params['temp'][1]), 1),
                'humidity': np.round(np.random.uniform(params['humidity'][0], params['humidity'][1]), 1),
                'ph': np.round(np.random.uniform(params['pH'][0], params['pH'][1]), 2),
                'rainfall': np.round(np.random.uniform(params['rainfall'][0], params['rainfall'][1]), 1),
                'label': crop
            }
            data.append(sample)
    
    df = pd.DataFrame(data)
    print(f"✅ Generated dataset with {len(df)} samples across {len(crops)} crops")
    return df

def train_standard_model():
    """Train the best performing standard crop recommendation model"""
    print("🤖 Training Standard Crop Recommendation Model")
    print("=" * 50)
    
    # Create comprehensive dataset
    df = create_comprehensive_dataset()
    
    # Prepare features and target
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    print(f"📊 Dataset shape: {X.shape}")
    print(f"🏷️ Number of crops: {y.nunique()}")
    print(f"📋 Crops: {sorted(y.unique())}")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Initialize models for ensemble
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            max_depth=8,
            learning_rate=0.1,
            random_state=42
        ),
        'Decision Tree': DecisionTreeClassifier(
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
    }
    
    print("\n🔍 Training and evaluating individual models...")
    best_model = None
    best_score = 0
    model_scores = {}
    
    for name, model in models.items():
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        mean_cv_score = cv_scores.mean()
        model_scores[name] = mean_cv_score
        
        # Train on full training set
        model.fit(X_train, y_train)
        
        # Test accuracy
        test_score = model.score(X_test, y_test)
        
        print(f"   {name}:")
        print(f"     CV Score: {mean_cv_score:.4f} (±{cv_scores.std()*2:.4f})")
        print(f"     Test Score: {test_score:.4f}")
        
        if test_score > best_score:
            best_score = test_score
            best_model = model
            best_model_name = name
    
    print(f"\n🏆 Best Model: {best_model_name} with {best_score:.4f} accuracy")
    
    # Create ensemble model for even better performance
    print("\n🤝 Creating ensemble model...")
    ensemble_model = VotingClassifier(
        estimators=[
            ('rf', models['Random Forest']),
            ('gb', models['Gradient Boosting']),
            ('dt', models['Decision Tree'])
        ],
        voting='soft'
    )
    
    ensemble_model.fit(X_train, y_train)
    ensemble_score = ensemble_model.score(X_test, y_test)
    
    print(f"🎯 Ensemble Model Score: {ensemble_score:.4f}")
    
    # Choose the best performing model
    if ensemble_score > best_score:
        final_model = ensemble_model
        final_score = ensemble_score
        final_model_name = "Ensemble"
    else:
        final_model = best_model
        final_score = best_score
        final_model_name = best_model_name
    
    print(f"\n🎉 Final Model: {final_model_name} with {final_score:.4f} accuracy")
    
    # Detailed evaluation
    print("\n📈 Detailed Evaluation:")
    y_pred = final_model.predict(X_test)
    print(f"Test Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    # Feature importance (if available)
    if hasattr(final_model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': final_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🔍 Feature Importance:")
        for _, row in feature_importance.iterrows():
            print(f"   {row['feature']}: {row['importance']:.4f}")
    
    # Save the model
    model_path = 'crop_recommendation_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(final_model, f)
    
    print(f"\n✅ Model saved as '{model_path}'")
    
    # Test with sample prediction
    print("\n🧪 Testing model with sample predictions:")
    test_samples = [
        [90, 42, 43, 20.87, 82.00, 6.50, 202.93],  # Should predict rice
        [85, 58, 41, 21.77, 80.31, 7.03, 226.65],  # Should predict rice  
        [60, 55, 44, 23.00, 82.32, 7.84, 263.96],  # Should predict rice
        [74, 35, 40, 26.49, 80.15, 6.98, 242.86]   # Should predict rice
    ]
    
    for i, sample in enumerate(test_samples):
        prediction = final_model.predict([sample])[0]
        if hasattr(final_model, 'predict_proba'):
            confidence = final_model.predict_proba([sample]).max()
            print(f"   Sample {i+1}: {prediction} (confidence: {confidence:.3f})")
        else:
            print(f"   Sample {i+1}: {prediction}")
    
    # Create model info dictionary
    model_info = {
        'model': final_model,
        'accuracy': final_score,
        'model_type': final_model_name,
        'features': list(X.columns),
        'crops': sorted(y.unique()),
        'training_samples': len(X_train),
        'test_samples': len(X_test)
    }
    
    return model_info

def validate_model():
    """Validate the saved model"""
    print("\n🔍 Validating saved model...")
    
    try:
        with open('crop_recommendation_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Test prediction
        test_input = [[90, 42, 43, 20.87, 82.00, 6.50, 202.93]]  # Rice parameters
        prediction = model.predict(test_input)
        
        print(f"✅ Model validation successful!")
        print(f"   Test prediction: {prediction[0]}")
        
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(test_input)
            confidence = proba.max()
            print(f"   Confidence: {confidence:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model validation failed: {e}")
        return False

if __name__ == "__main__":
    print("🌾 Standard Crop Recommendation Model Training")
    print("=" * 55)
    
    # Train the model
    model_info = train_standard_model()
    
    # Validate the saved model
    validation_success = validate_model()
    
    # Summary
    print(f"\n📋 Training Summary:")
    print(f"   Model Type: {model_info['model_type']}")
    print(f"   Accuracy: {model_info['accuracy']:.4f}")
    print(f"   Features: {len(model_info['features'])}")
    print(f"   Crops: {len(model_info['crops'])}")
    print(f"   Training Samples: {model_info['training_samples']}")
    print(f"   Test Samples: {model_info['test_samples']}")
    print(f"   Validation: {'✅ Passed' if validation_success else '❌ Failed'}")
    
    if validation_success:
        print(f"\n🎉 Standard model successfully created and ready to use!")
        print(f"   File: crop_recommendation_model.pkl")
        print(f"   Size: {os.path.getsize('crop_recommendation_model.pkl')} bytes")
    else:
        print(f"\n❌ Model creation failed!")
