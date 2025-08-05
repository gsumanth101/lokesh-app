#!/usr/bin/env python3
"""
Improved Market Trends Predictor
Creates a model with proper encoder handling for consistent predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MarketTrendsPredictor:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']
        self.target_column = 'Modal_x0020_Price'
        
    def prepare_data(self, data):
        """Prepare data for training or prediction"""
        df = data.copy()
        
        # Clean the data
        df = df.dropna(subset=self.feature_columns + [self.target_column])
        
        # Remove any rows with zero or negative prices
        df = df[df[self.target_column] > 0]
        
        return df
    
    def encode_features(self, data, fit=False):
        """Encode categorical features using label encoders"""
        df = data.copy()
        
        for column in self.feature_columns:
            if fit:
                # Create and fit encoder during training
                self.encoders[column] = LabelEncoder()
                df[column] = self.encoders[column].fit_transform(df[column].astype(str))
            else:
                # Use existing encoder for prediction
                if column in self.encoders:
                    # Handle unknown categories by adding them to the encoder
                    unknown_labels = set(df[column].astype(str)) - set(self.encoders[column].classes_)
                    if unknown_labels:
                        # Add unknown labels to encoder classes
                        self.encoders[column].classes_ = np.append(
                            self.encoders[column].classes_, 
                            list(unknown_labels)
                        )
                    df[column] = self.encoders[column].transform(df[column].astype(str))
                else:
                    raise ValueError(f"Encoder for {column} not found. Model needs to be trained first.")
        
        return df
    
    def train_model(self, data_path):
        """Train the prediction model"""
        print("Loading and preparing data...")
        
        # Load data
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} records")
        
        # Prepare data
        df_clean = self.prepare_data(df)
        print(f"After cleaning: {len(df_clean)} records")
        
        # Encode features
        df_encoded = self.encode_features(df_clean, fit=True)
        
        # Prepare features and target
        X = df_encoded[self.feature_columns]
        y = df_encoded[self.target_column]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        print("Training model...")
        
        # Try Random Forest (usually better for this type of data)
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        train_mse = mean_squared_error(y_train, train_pred)
        test_mse = mean_squared_error(y_test, test_pred)
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        
        print(f"\nModel Performance:")
        print(f"Training MSE: {train_mse:.2f}")
        print(f"Testing MSE: {test_mse:.2f}")
        print(f"Training R²: {train_r2:.4f}")
        print(f"Testing R²: {test_r2:.4f}")
        
        # Show feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(f"\nFeature Importance:")
        for _, row in feature_importance.iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")
        
        return test_r2
    
    def predict_price(self, features):
        """Predict price for given features"""
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        # Convert single prediction to DataFrame
        if isinstance(features, dict):
            df = pd.DataFrame([features])
        else:
            df = features.copy()
        
        # Ensure all required columns are present
        for col in self.feature_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required feature: {col}")
        
        # Encode features
        df_encoded = self.encode_features(df, fit=False)
        
        # Select and scale features
        X = df_encoded[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)
        
        return prediction[0] if len(prediction) == 1 else prediction
    
    def save_model(self, model_path='market_predictor_model.pkl'):
        """Save the trained model and encoders"""
        model_data = {
            'model': self.model,
            'encoders': self.encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='market_predictor_model.pkl'):
        """Load a trained model and encoders"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.encoders = model_data['encoders']
            self.scaler = model_data['scaler']
            self.feature_columns = model_data['feature_columns']
            self.target_column = model_data['target_column']
            
            print(f"Model loaded from {model_path}")
            return True
            
        except FileNotFoundError:
            print(f"Model file {model_path} not found")
            return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

def create_and_train_model():
    """Create and train a new market prediction model"""
    print("=== Market Trends Predictor Training ===\n")
    
    # Initialize predictor
    predictor = MarketTrendsPredictor()
    
    # Train the model
    data_path = 'data/markettrends.csv'
    r2_score = predictor.train_model(data_path)
    
    # Save the model
    predictor.save_model('improved_market_model.pkl')
    
    print(f"\n✅ Model training completed with R² score: {r2_score:.4f}")
    
    return predictor

def test_predictions(predictor):
    """Test the predictor with sample data"""
    print("\n=== Testing Predictions ===\n")
    
    # Test cases
    test_cases = [
        {
            'State': 'Andhra Pradesh',
            'District': 'Guntur',
            'Market': 'Guntur',
            'Commodity': 'Rice',
            'Variety': 'Common',
            'Grade': 'FAQ'
        },
        {
            'State': 'Gujarat',
            'District': 'Ahmedabad',
            'Market': 'Ahmedabad',
            'Commodity': 'Wheat',
            'Variety': 'Other',
            'Grade': 'FAQ'
        },
        {
            'State': 'Maharashtra',
            'District': 'Pune',
            'Market': 'Pune',
            'Commodity': 'Onion',
            'Variety': 'Medium',
            'Grade': 'FAQ'
        },
        {
            'State': 'Haryana',
            'District': 'Karnal',
            'Market': 'Karnal',
            'Commodity': 'Potato',
            'Variety': 'Other',
            'Grade': 'FAQ'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            predicted_price = predictor.predict_price(test_case)
            print(f"{i}. {test_case['Commodity']} in {test_case['State']}")
            print(f"   Market: {test_case['Market']}")
            print(f"   Predicted Price: ₹{predicted_price:.2f}/quintal")
            print()
        except Exception as e:
            print(f"{i}. Error predicting for {test_case['Commodity']}: {e}")
            print()

def main():
    """Main function"""
    # Create and train new model
    predictor = create_and_train_model()
    
    # Test the model
    test_predictions(predictor)
    
    print("=== Model Creation Complete ===")
    print("You can now use 'improved_market_model.pkl' for predictions!")

if __name__ == "__main__":
    main()
