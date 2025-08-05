import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import warnings
warnings.filterwarnings('ignore')

def create_comprehensive_dataset():
    """Create a comprehensive dataset for crop recommendation with realistic data"""
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create a balanced crop dataset with distinct characteristics
    crops_data = []
    
    # Wheat data - Cool season crop
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(20, 3),  # Cooler temperatures
            'humidity': np.random.normal(55, 8),
            'N': np.random.normal(80, 15),
            'P': np.random.normal(30, 8),
            'K': np.random.normal(40, 10),
            'pH': np.random.normal(6.8, 0.3),
            'rainfall': np.random.normal(500, 100),
            'crop': 'wheat'
        })
    
    # Rice data - High humidity, high rainfall
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(28, 2),
            'humidity': np.random.normal(85, 5),  # High humidity
            'N': np.random.normal(110, 20),
            'P': np.random.normal(40, 10),
            'K': np.random.normal(50, 12),
            'pH': np.random.normal(6.2, 0.4),
            'rainfall': np.random.normal(1500, 200),  # High rainfall
            'crop': 'rice'
        })
    
    # Maize data - Moderate conditions
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(25, 2),
            'humidity': np.random.normal(70, 8),
            'N': np.random.normal(100, 15),
            'P': np.random.normal(60, 12),
            'K': np.random.normal(40, 8),
            'pH': np.random.normal(6.5, 0.3),
            'rainfall': np.random.normal(900, 150),
            'crop': 'maize'
        })
    
    # Cotton data - Warm, high N and K
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(30, 3),  # Warmer
            'humidity': np.random.normal(65, 10),
            'N': np.random.normal(140, 20),  # High N
            'P': np.random.normal(35, 8),
            'K': np.random.normal(125, 15),  # High K
            'pH': np.random.normal(6.8, 0.4),
            'rainfall': np.random.normal(750, 120),
            'crop': 'cotton'
        })
    
    # Sugarcane data - Very warm, high humidity
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(32, 2),  # Very warm
            'humidity': np.random.normal(80, 8),
            'N': np.random.normal(125, 18),
            'P': np.random.normal(40, 10),
            'K': np.random.normal(75, 12),
            'pH': np.random.normal(6.8, 0.3),
            'rainfall': np.random.normal(1250, 180),
            'crop': 'sugarcane'
        })
    
    # Tomato data - Moderate temp, high P
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(24, 3),
            'humidity': np.random.normal(70, 8),
            'N': np.random.normal(100, 15),
            'P': np.random.normal(65, 12),  # High P
            'K': np.random.normal(75, 10),
            'pH': np.random.normal(6.5, 0.2),
            'rainfall': np.random.normal(600, 100),
            'crop': 'tomato'
        })
    
    # Potato data - Cool, high N and K
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(18, 2),  # Cool
            'humidity': np.random.normal(80, 8),
            'N': np.random.normal(120, 15),
            'P': np.random.normal(60, 10),
            'K': np.random.normal(100, 12),  # High K
            'pH': np.random.normal(6.0, 0.3),  # Slightly acidic
            'rainfall': np.random.normal(550, 80),
            'crop': 'potato'
        })
    
    # Onion data - Moderate conditions
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(23, 2),
            'humidity': np.random.normal(60, 8),
            'N': np.random.normal(80, 12),
            'P': np.random.normal(45, 8),
            'K': np.random.normal(60, 10),
            'pH': np.random.normal(6.8, 0.3),
            'rainfall': np.random.normal(800, 100),
            'crop': 'onion'
        })
    
    # Barley data - Cool, low rainfall
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(18, 2),  # Cool
            'humidity': np.random.normal(55, 8),
            'N': np.random.normal(80, 12),
            'P': np.random.normal(35, 8),
            'K': np.random.normal(45, 8),
            'pH': np.random.normal(6.8, 0.3),
            'rainfall': np.random.normal(450, 80),  # Low rainfall
            'crop': 'barley'
        })
    
    # Millet data - Very hot, drought resistant, low rainfall
    for i in range(100):
        crops_data.append({
            'temperature': np.random.normal(35, 2),  # Very hot
            'humidity': np.random.normal(50, 8),  # Low humidity
            'N': np.random.normal(60, 10),  # Low N
            'P': np.random.normal(25, 5),  # Low P
            'K': np.random.normal(35, 8),  # Low K
            'pH': np.random.normal(6.5, 0.4),
            'rainfall': np.random.normal(300, 50),  # Very low rainfall
            'crop': 'millet'
        })
    
    # Clean the data to ensure positive values
    df = pd.DataFrame(crops_data)
    
    # Ensure all values are positive
    df['temperature'] = np.clip(df['temperature'], 10, 45)
    df['humidity'] = np.clip(df['humidity'], 30, 95)
    df['N'] = np.clip(df['N'], 20, 200)
    df['P'] = np.clip(df['P'], 10, 100)
    df['K'] = np.clip(df['K'], 15, 180)
    df['pH'] = np.clip(df['pH'], 5.0, 8.5)
    df['rainfall'] = np.clip(df['rainfall'], 200, 2000)
    
    return df

def train_models():
    """Train multiple models and select the best one"""
    
    print("Creating comprehensive dataset...")
    df = create_comprehensive_dataset()
    
    # Save the dataset
    df.to_csv('data/comprehensive_crop_data.csv', index=False)
    print("Dataset saved to data/comprehensive_crop_data.csv")
    
    # Features and target
    X = df[['temperature', 'humidity', 'N', 'P', 'K', 'pH', 'rainfall']]
    y = df['crop']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest with hyperparameter tuning
    print("Training Random Forest with hyperparameter tuning...")
    rf_model = RandomForestClassifier(n_estimators=300, random_state=42, max_depth=15, min_samples_split=5, min_samples_leaf=3)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    print(f"Optimized Random Forest Accuracy: {rf_accuracy:.3f}")
    
    # Use Random Forest as the best model
    best_model = rf_model
    best_name = "Random Forest"
    print(f"Selected Random Forest as the best model with accuracy: {rf_accuracy:.3f}")
    
    # Save the best model
    with open('crop_recommendation_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    print(f"Best model ({best_name}) saved as crop_recommendation_model.pkl")
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, rf_pred))
    
    # Feature importance
    feature_names = ['temperature', 'humidity', 'N', 'P', 'K', 'pH', 'rainfall']
    feature_importance = best_model.feature_importances_
    
    print("\nFeature Importance:")
    for name, importance in zip(feature_names, feature_importance):
        print(f"{name}: {importance:.3f}")

if __name__ == "__main__":
    train_models()
