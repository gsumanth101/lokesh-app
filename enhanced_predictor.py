#!/usr/bin/env python3
"""
Enhanced Market Trends Predictor for All Commodities
Handles more commodities with consistent encoding and training
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle

class ComprehensiveTrendsPredictor:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']
        self.target_column = 'Modal_x0020_Price'
        
    def prepare_data(self, data):
        """Prepare data for all commodities"""
        df = data.copy()
        df = df.dropna(subset=self.feature_columns + [self.target_column])
        df = df[df[self.target_column] > 0]
        return df
    
    def encode_features(self, data, fit=False):
        """Encode features, updating encoders for training"""
        df = data.copy()
        
        for column in self.feature_columns:
            if fit:
                self.encoders[column] = LabelEncoder()
                df[column] = self.encoders[column].fit_transform(df[column].astype(str))
            else:
                if column in self.encoders:
                    unknown_labels = set(df[column].astype(str)) - set(self.encoders[column].classes_)
                    if unknown_labels:
                        self.encoders[column].classes_ = np.append(
                            self.encoders[column].classes_, 
                            list(unknown_labels)
                        )
                    df[column] = self.encoders[column].transform(df[column].astype(str))
                else:
                    raise ValueError(f"Encoder for {column} not found.")
        
        return df
    
    def train_model(self, data_path):
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} records")
        df_clean = self.prepare_data(df)
        print(f"After cleaning: {len(df_clean)} records")
        df_encoded = self.encode_features(df_clean, fit=True)
        
        X = df_encoded[self.feature_columns]
        y = df_encoded[self.target_column]
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
        self.model.fit(X_train, y_train)
        
        train_mse = mean_squared_error(y_train, self.model.predict(X_train))
        test_mse = mean_squared_error(y_test, self.model.predict(X_test))
        print(f"Training MSE: {train_mse:.2f}, Testing MSE: {test_mse:.2f}")
        
        return r2_score(y_test, self.model.predict(X_test))
    
    def predict_price(self, features):
        if self.model is None:
            raise ValueError("Model not trained.")
        df = pd.DataFrame([features])
        df_encoded = self.encode_features(df, fit=False)
        X_scaled = self.scaler.transform(df_encoded[self.feature_columns])
        prediction = self.model.predict(X_scaled)
        return prediction[0]
    
    def save_model(self, model_path='full_market_model.pkl'):
        model_data = {
            'model': self.model,
            'encoders': self.encoders,
            'scaler': self.scaler
        }
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='full_market_model.pkl'):
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            self.model = model_data['model']
            self.encoders = model_data['encoders']
            self.scaler = model_data['scaler']
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

def create_and_test_model(data_path='data/markettrends.csv'):
    predictor = ComprehensiveTrendsPredictor()
    r2 = predictor.train_model(data_path)
    predictor.save_model()
    print(f"Model trained with R²: {r2:.4f}")
    return predictor

def main():
    predictor = create_and_test_model()
    features = {
        'State': 'Karnataka',
        'District': 'Bangalore',
        'Market': 'Ramanagara',
        'Commodity': 'Tomato',
        'Variety': 'Other',
        'Grade': 'FAQ'
    }
    try:
        price = predictor.predict_price(features)
        print(f"Predicted price for Tomato in Bangalore: ₹{price:.2f}/quintal")
    except Exception as ex:
        print(f"Prediction error: {ex}")

if __name__ == "__main__":
    main()
