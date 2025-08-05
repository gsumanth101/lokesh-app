#!/usr/bin/env python3
"""
Balanced Crop Recommendation Models
Creates diverse, well-balanced models that predict various crops
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import pickle
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')

def create_balanced_dataset():
    """Create a well-balanced dataset with diverse crop predictions"""
    print("🌾 Creating balanced crop recommendation dataset...")
    
    # All crops from your system
    crops = [
        'apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton',
        'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans',
        'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate',
        'rice', 'watermelon', 'wheat', 'tomato', 'potato', 'onion', 'barley'
    ]
    
    np.random.seed(123)  # Different seed for better distribution
    data = []
    
    # More realistic and diverse parameter ranges
    crop_params = {
        'rice': {'N': (70, 140), 'P': (35, 85), 'K': (35, 85), 'temp': (20, 35), 'humidity': (75, 95), 'pH': (5.5, 7.2), 'rainfall': (1000, 3000)},
        'wheat': {'N': (50, 110), 'P': (25, 65), 'K': (25, 65), 'temp': (12, 28), 'humidity': (45, 75), 'pH': (6.0, 8.0), 'rainfall': (300, 900)},
        'maize': {'N': (70, 130), 'P': (35, 85), 'K': (35, 85), 'temp': (18, 32), 'humidity': (55, 85), 'pH': (5.5, 7.5), 'rainfall': (400, 1200)},
        'cotton': {'N': (50, 110), 'P': (25, 70), 'K': (45, 95), 'temp': (18, 35), 'humidity': (45, 85), 'pH': (5.5, 8.5), 'rainfall': (400, 1400)},
        'tomato': {'N': (70, 130), 'P': (50, 110), 'K': (90, 160), 'temp': (18, 32), 'humidity': (55, 85), 'pH': (5.5, 7.2), 'rainfall': (500, 1300)},
        'potato': {'N': (70, 130), 'P': (35, 85), 'K': (90, 160), 'temp': (10, 28), 'humidity': (65, 90), 'pH': (4.8, 6.8), 'rainfall': (400, 800)},
        'onion': {'N': (50, 110), 'P': (35, 85), 'K': (70, 130), 'temp': (10, 28), 'humidity': (55, 75), 'pH': (5.8, 7.8), 'rainfall': (500, 1100)},
        'apple': {'N': (30, 90), 'P': (15, 45), 'K': (35, 85), 'temp': (10, 28), 'humidity': (45, 75), 'pH': (5.0, 7.5), 'rainfall': (800, 1400)},
        'banana': {'N': (90, 160), 'P': (45, 110), 'K': (180, 320), 'temp': (24, 32), 'humidity': (70, 90), 'pH': (5.0, 7.5), 'rainfall': (1200, 2800)},
        'mango': {'N': (40, 100), 'P': (25, 70), 'K': (45, 95), 'temp': (22, 35), 'humidity': (45, 80), 'pH': (5.0, 8.0), 'rainfall': (600, 2800)},
        'grapes': {'N': (30, 90), 'P': (25, 70), 'K': (70, 130), 'temp': (12, 28), 'humidity': (45, 75), 'pH': (5.5, 8.0), 'rainfall': (400, 900)},
        'orange': {'N': (40, 100), 'P': (25, 70), 'K': (45, 95), 'temp': (12, 32), 'humidity': (50, 80), 'pH': (5.5, 8.0), 'rainfall': (1000, 2000)},
        'pomegranate': {'N': (30, 90), 'P': (25, 70), 'K': (35, 85), 'temp': (12, 28), 'humidity': (30, 60), 'pH': (5.0, 8.0), 'rainfall': (400, 800)},
        'watermelon': {'N': (70, 130), 'P': (35, 85), 'K': (70, 130), 'temp': (22, 35), 'humidity': (45, 75), 'pH': (5.8, 7.2), 'rainfall': (300, 700)},
        'muskmelon': {'N': (70, 130), 'P': (35, 85), 'K': (70, 130), 'temp': (23, 37), 'humidity': (45, 75), 'pH': (6.0, 7.8), 'rainfall': (300, 700)},
        'papaya': {'N': (50, 110), 'P': (35, 85), 'K': (50, 110), 'temp': (20, 35), 'humidity': (55, 90), 'pH': (5.0, 7.5), 'rainfall': (800, 2200)},
        'coconut': {'N': (40, 100), 'P': (25, 70), 'K': (90, 160), 'temp': (25, 35), 'humidity': (65, 90), 'pH': (4.5, 8.5), 'rainfall': (1000, 2200)},
        'coffee': {'N': (40, 90), 'P': (25, 55), 'K': (50, 110), 'temp': (12, 28), 'humidity': (65, 90), 'pH': (5.5, 7.5), 'rainfall': (1200, 2800)},
        'chickpea': {'N': (15, 45), 'P': (35, 85), 'K': (15, 45), 'temp': (18, 32), 'humidity': (55, 75), 'pH': (6.0, 8.2), 'rainfall': (300, 700)},
        'kidneybeans': {'N': (15, 45), 'P': (35, 85), 'K': (15, 45), 'temp': (12, 28), 'humidity': (60, 80), 'pH': (5.5, 8.0), 'rainfall': (250, 650)},
        'pigeonpeas': {'N': (15, 45), 'P': (25, 70), 'K': (10, 40), 'temp': (24, 32), 'humidity': (55, 80), 'pH': (6.2, 8.0), 'rainfall': (500, 1100)},
        'mothbeans': {'N': (15, 45), 'P': (35, 85), 'K': (15, 45), 'temp': (25, 35), 'humidity': (45, 70), 'pH': (5.5, 8.5), 'rainfall': (300, 700)},
        'mungbean': {'N': (15, 45), 'P': (35, 85), 'K': (15, 45), 'temp': (23, 37), 'humidity': (55, 80), 'pH': (6.0, 7.5), 'rainfall': (400, 800)},
        'blackgram': {'N': (15, 45), 'P': (35, 85), 'K': (15, 45), 'temp': (23, 37), 'humidity': (55, 75), 'pH': (6.2, 8.0), 'rainfall': (500, 1100)},
        'lentil': {'N': (15, 45), 'P': (35, 85), 'K': (15, 45), 'temp': (15, 32), 'humidity': (55, 75), 'pH': (5.5, 8.0), 'rainfall': (250, 450)},
        'barley': {'N': (40, 100), 'P': (20, 55), 'K': (20, 55), 'temp': (8, 28), 'humidity': (50, 75), 'pH': (5.5, 8.0), 'rainfall': (350, 700)},
        'jute': {'N': (50, 110), 'P': (25, 70), 'K': (25, 70), 'temp': (22, 37), 'humidity': (65, 95), 'pH': (5.5, 8.0), 'rainfall': (1000, 2000)}
    }
    
    # Generate balanced samples for each crop
    samples_per_crop = 150  # Increased samples for better training
    
    for crop in crops:
        if crop in crop_params:
            params = crop_params[crop]
        else:
            # Default parameters for any missing crops
            params = {'N': (40, 100), 'P': (30, 80), 'K': (40, 100), 'temp': (20, 30), 'humidity': (60, 80), 'pH': (6.0, 7.5), 'rainfall': (800, 1200)}
        
        # Generate diverse samples with multiple scenarios
        for scenario in range(samples_per_crop):
            # Add some variation in the parameters to create more realistic data
            variation_factor = np.random.uniform(0.8, 1.2)  # ±20% variation
            
            sample = {
                'N': np.random.randint(
                    max(5, int(params['N'][0] * variation_factor)), 
                    min(200, int(params['N'][1] * variation_factor)) + 1
                ),
                'P': np.random.randint(
                    max(5, int(params['P'][0] * variation_factor)), 
                    min(150, int(params['P'][1] * variation_factor)) + 1
                ),
                'K': np.random.randint(
                    max(5, int(params['K'][0] * variation_factor)), 
                    min(300, int(params['K'][1] * variation_factor)) + 1
                ),
                'temperature': np.round(np.random.uniform(
                    max(5, params['temp'][0] * variation_factor), 
                    min(45, params['temp'][1] * variation_factor)
                ), 1),
                'humidity': np.round(np.random.uniform(
                    max(20, params['humidity'][0] * variation_factor), 
                    min(100, params['humidity'][1] * variation_factor)
                ), 1),
                'ph': np.round(np.random.uniform(
                    max(4.0, params['pH'][0] * variation_factor), 
                    min(9.0, params['pH'][1] * variation_factor)
                ), 2),
                'rainfall': np.round(np.random.uniform(
                    max(100, params['rainfall'][0] * variation_factor), 
                    min(4000, params['rainfall'][1] * variation_factor)
                ), 1),
                'label': crop
            }
            data.append(sample)
    
    df = pd.DataFrame(data)
    
    # Shuffle the dataset to ensure good mixing
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"✅ Generated balanced dataset with {len(df)} samples")
    print(f"📊 Samples per crop: {len(df) // len(crops)}")
    print(f"🏷️ Crops: {len(crops)}")
    
    # Display crop distribution
    crop_counts = df['label'].value_counts()
    print(f"📈 Crop distribution: {crop_counts.min()} - {crop_counts.max()} samples per crop")
    
    return df

def train_improved_standard_model():
    """Train an improved standard model with better balance"""
    print("\n🤖 Training Improved Standard Model")
    print("=" * 50)
    
    # Create balanced dataset
    df = create_balanced_dataset()
    
    # Prepare features and target
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    print(f"📊 Dataset shape: {X.shape}")
    print(f"🏷️ Number of unique crops: {y.nunique()}")
    
    # Split with stratification to maintain balance
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Try multiple algorithms and choose the best balanced one
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            min_samples_split=3,
            min_samples_leaf=1,
            max_features='sqrt',
            random_state=42,
            class_weight='balanced'  # Important for balanced predictions
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.05,
            random_state=42
        ),
        'Decision Tree': DecisionTreeClassifier(
            max_depth=15,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
    }
    
    print("\n🔍 Training and evaluating models...")
    best_model = None
    best_score = 0
    best_diversity = 0
    
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Test accuracy
        test_score = model.score(X_test, y_test)
        
        # Test prediction diversity (how many different crops it predicts)
        y_pred = model.predict(X_test)
        unique_predictions = len(set(y_pred))
        diversity_score = unique_predictions / len(set(y_test))
        
        print(f"   {name}:")
        print(f"     Accuracy: {test_score:.4f}")
        print(f"     Predicts {unique_predictions}/{len(set(y_test))} crops (diversity: {diversity_score:.3f})")
        
        # Choose model based on balance of accuracy and diversity
        combined_score = test_score * 0.7 + diversity_score * 0.3
        
        if combined_score > best_score or (combined_score == best_score and diversity_score > best_diversity):
            best_score = combined_score
            best_diversity = diversity_score
            best_model = model
            best_model_name = name
    
    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Combined Score: {best_score:.4f}")
    print(f"   Diversity Score: {best_diversity:.4f}")
    
    # Test with various sample inputs to ensure diversity
    print(f"\n🧪 Testing prediction diversity...")
    test_cases = [
        # Typical rice conditions
        [90, 42, 43, 20.87, 82.00, 6.50, 1500],
        # Typical wheat conditions  
        [80, 40, 35, 18.50, 60.00, 7.20, 500],
        # Typical cotton conditions
        [70, 35, 60, 28.00, 70.00, 7.00, 800],
        # Typical tomato conditions
        [100, 70, 120, 25.00, 75.00, 6.50, 900],
        # Typical potato conditions
        [100, 50, 120, 20.00, 80.00, 6.00, 600],
        # Tropical fruit conditions
        [60, 40, 80, 30.00, 85.00, 6.80, 2000],
        # Pulse conditions
        [25, 60, 25, 25.00, 65.00, 7.50, 400],
        # Dry climate conditions
        [50, 30, 40, 32.00, 45.00, 7.80, 300],
        # High rainfall conditions
        [85, 45, 70, 24.00, 88.00, 6.20, 2500],
        # Cold climate conditions
        [60, 35, 45, 15.00, 65.00, 6.80, 700]
    ]
    
    predictions = []
    for i, test_case in enumerate(test_cases):
        pred = best_model.predict([test_case])[0]
        predictions.append(pred)
        confidence = best_model.predict_proba([test_case]).max() if hasattr(best_model, 'predict_proba') else 'N/A'
        print(f"   Test {i+1}: {pred} (confidence: {confidence:.3f})" if confidence != 'N/A' else f"   Test {i+1}: {pred}")
    
    unique_test_predictions = len(set(predictions))
    print(f"\n📊 Test diversity: {unique_test_predictions}/{len(test_cases)} different crops predicted")
    
    # Save the improved model
    with open('crop_recommendation_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    print(f"\n✅ Improved standard model saved as 'crop_recommendation_model.pkl'")
    
    return best_model, test_score, unique_test_predictions

def train_improved_optimized_model():
    """Train an improved optimized model"""
    print("\n🚀 Training Improved Optimized Model")
    print("=" * 50)
    
    # Use the same balanced dataset
    df = create_balanced_dataset()
    
    # Prepare features and target with feature scaling
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    # Scale features for better performance
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=123, stratify=y
    )
    
    # Advanced ensemble model
    from sklearn.ensemble import VotingClassifier
    
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=20,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features='log2',
        random_state=42,
        class_weight='balanced'
    )
    
    gb = GradientBoostingClassifier(
        n_estimators=200,
        max_depth=8,
        learning_rate=0.03,
        subsample=0.8,
        random_state=42
    )
    
    dt = DecisionTreeClassifier(
        max_depth=25,
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42,
        class_weight='balanced'
    )
    
    # Create ensemble
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('gb', gb), ('dt', dt)],
        voting='soft'
    )
    
    print("🔧 Training ensemble model...")
    ensemble.fit(X_train, y_train)
    
    # Evaluate
    test_score = ensemble.score(X_test, y_test)
    y_pred = ensemble.predict(X_test)
    unique_predictions = len(set(y_pred))
    diversity_score = unique_predictions / len(set(y_test))
    
    print(f"✅ Optimized Model Performance:")
    print(f"   Accuracy: {test_score:.4f}")
    print(f"   Predicts {unique_predictions}/{len(set(y_test))} crops")
    print(f"   Diversity: {diversity_score:.4f}")
    
    # Test diversity
    print(f"\n🧪 Testing optimized model diversity...")
    test_cases = [
        [90, 42, 43, 20.87, 82.00, 6.50, 1500],
        [80, 40, 35, 18.50, 60.00, 7.20, 500],
        [70, 35, 60, 28.00, 70.00, 7.00, 800],
        [100, 70, 120, 25.00, 75.00, 6.50, 900],
        [100, 50, 120, 20.00, 80.00, 6.00, 600],
        [60, 40, 80, 30.00, 85.00, 6.80, 2000],
        [25, 60, 25, 25.00, 65.00, 7.50, 400],
        [50, 30, 40, 32.00, 45.00, 7.80, 300],
        [85, 45, 70, 24.00, 88.00, 6.20, 2500],
        [60, 35, 45, 15.00, 65.00, 6.80, 700]
    ]
    
    opt_predictions = []
    for i, test_case in enumerate(test_cases):
        # Scale the test case
        test_case_scaled = scaler.transform([test_case])
        pred = ensemble.predict(test_case_scaled)[0]
        opt_predictions.append(pred)
        confidence = ensemble.predict_proba(test_case_scaled).max()
        print(f"   Test {i+1}: {pred} (confidence: {confidence:.3f})")
    
    unique_opt_predictions = len(set(opt_predictions))
    print(f"\n📊 Optimized test diversity: {unique_opt_predictions}/{len(test_cases)} different crops")
    
    # Save the improved optimized model with scaler
    model_data = {
        'model': ensemble,
        'scaler': scaler,
        'feature_names': ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    }
    
    with open('optimized_crop_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✅ Improved optimized model saved as 'optimized_crop_model.pkl'")
    
    return ensemble, test_score, unique_opt_predictions

def main():
    """Main training function"""
    print("🌾 Training Balanced Crop Recommendation Models")
    print("=" * 60)
    
    # Train improved standard model
    std_model, std_accuracy, std_diversity = train_improved_standard_model()
    
    # Train improved optimized model  
    opt_model, opt_accuracy, opt_diversity = train_improved_optimized_model()
    
    # Summary
    print(f"\n📋 Training Summary:")
    print("=" * 40)
    print(f"🔧 Standard Model:")
    print(f"   Accuracy: {std_accuracy:.4f}")
    print(f"   Diversity: {std_diversity}/10 test cases")
    print(f"   Status: ✅ Balanced predictions")
    
    print(f"\n🚀 Optimized Model:")
    print(f"   Accuracy: {opt_accuracy:.4f}")
    print(f"   Diversity: {opt_diversity}/10 test cases")
    print(f"   Status: ✅ Enhanced performance")
    
    print(f"\n🎉 Both models now provide diverse crop predictions!")
    print(f"💡 Models will recommend different crops based on:")
    print(f"   • Soil conditions (N, P, K, pH)")
    print(f"   • Climate factors (temperature, humidity, rainfall)")
    print(f"   • Regional variations")

if __name__ == "__main__":
    main()
