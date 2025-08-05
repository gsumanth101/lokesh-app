import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

def train_optimized_crop_model():
    """
    Train crop recommendation model with selected features:
    - Weather data (from NASA Power API): temperature, humidity, rainfall, wind_speed, sunlight_exposure
    - Soil health (user input): N, P, K, pH, soil_moisture, soil_type, organic_matter
    - Water source (user input): water_source_type
    - Environmental (calculated): co2_concentration
    """
    
    print("Loading dataset...")
    try:
        # Load the dataset
        df = pd.read_csv('data/Crop_recommendationV2.csv')
        print(f"Dataset loaded successfully with {len(df)} records")
        
        # Check for required columns
        required_columns = [
            'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label',
            'soil_moisture', 'soil_type', 'sunlight_exposure', 'wind_speed', 
            'co2_concentration', 'organic_matter', 'water_source_type'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Missing columns: {missing_columns}")
            return None
        
        # Select only the features we want to use
        selected_features = [
            # Weather data (will be fetched from NASA Power API)
            'temperature',           # NASA Power API
            'humidity',             # NASA Power API  
            'rainfall',             # NASA Power API
            'wind_speed',           # NASA Power API
            'sunlight_exposure',    # NASA Power API (solar radiation)
            
            # Soil health parameters (user input)
            'N',                    # User input
            'P',                    # User input
            'K',                    # User input
            'ph',                   # User input
            'organic_matter',       # User input
            
            # Location-based parameters (API derived)
            'soil_moisture',        # API derived from location
            'soil_type',            # API derived from location
            
            # Environmental factors
            'co2_concentration',    # Default/calculated value
            'water_source_type'     # User input
        ]
        
        # Prepare features and target
        X = df[selected_features].copy()
        y = df['label'].copy()
        
        print(f"Selected features: {selected_features}")
        print(f"Feature matrix shape: {X.shape}")
        print(f"Target classes: {y.unique()}")
        
        # Encode categorical variables
        le_soil_type = LabelEncoder()
        le_water_source = LabelEncoder()
        
        X['soil_type'] = le_soil_type.fit_transform(X['soil_type'])
        X['water_source_type'] = le_water_source.fit_transform(X['water_source_type'])
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set size: {X_train.shape[0]}")
        print(f"Testing set size: {X_test.shape[0]}")
        
        # Train the model
        print("Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
        
        # Print classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': selected_features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        # Save the model and encoders
        model_data = {
            'model': model,
            'feature_names': selected_features,
            'soil_type_encoder': le_soil_type,
            'water_source_encoder': le_water_source,
            'accuracy': accuracy,
            'feature_importance': feature_importance
        }
        
        with open('optimized_crop_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print("\nModel saved as 'optimized_crop_model.pkl'")
        
        # Print feature mappings
        print("\nSoil Type Mappings:")
        for i, label in enumerate(le_soil_type.classes_):
            print(f"{label}: {i}")
        
        print("\nWater Source Mappings:")
        for i, label in enumerate(le_water_source.classes_):
            print(f"{label}: {i}")
        
        return model_data
        
    except Exception as e:
        print(f"Error during training: {e}")
        return None

if __name__ == "__main__":
    print("Training Optimized Crop Recommendation Model")
    print("=" * 50)
    
    model_data = train_optimized_crop_model()
    
    if model_data:
        print("\nTraining completed successfully!")
        print(f"Model accuracy: {model_data['accuracy']:.4f}")
        print("\nTop 5 most important features:")
        print(model_data['feature_importance'].head())
    else:
        print("\nTraining failed!")
