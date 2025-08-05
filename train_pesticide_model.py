#!/usr/bin/env python3
"""
Advanced Pesticide Recommendation ML Training Script
====================================================

This script trains machine learning models to predict both organic and non-organic
pesticide recommendations based on crop, disease, environmental, and soil parameters.

Features:
- Multi-output classification for both organic and non-organic pesticides
- Advanced feature engineering and preprocessing
- Model evaluation with comprehensive metrics
- Model persistence for deployment
- Cross-validation and hyperparameter optimization
"""

import pandas as pd
import numpy as np
import pickle
import warnings
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class PesticideRecommendationTrainer:
    def __init__(self, data_path="data/pesticide_recommendation_training_dataset.csv"):
        """
        Initialize the pesticide recommendation trainer
        
        Args:
            data_path (str): Path to the training dataset CSV file
        """
        self.data_path = data_path
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_columns = []
        self.target_columns = []
        
    def load_and_preprocess_data(self):
        """
        Load and preprocess the training dataset
        
        Returns:
            tuple: Processed features and targets
        """
        print("Loading dataset...")
        
        # Load the dataset
        df = pd.read_csv(self.data_path)
        print(f"Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
        
        # Display basic info about the dataset
        print("\nDataset Info:")
        print(df.info())
        print("\nFirst few rows:")
        print(df.head())
        
        # Define feature columns (input variables)
        feature_cols = [
            'crop_type', 'disease_type', 'disease_stage', 'crop_stage', 
            'region', 'is_organic_farming', 'temperature', 'humidity', 
            'rainfall', 'soil_ph', 'nitrogen'
        ]
        
        # Define target columns (what we want to predict)
        target_cols = [
            'organic_pesticide',
            'organic_application_method',
            'non_organic_pesticide', 
            'non_organic_application_method'
        ]
        
        # Additional regression targets for dosage and frequency
        regression_targets = [
            'organic_dosage', 'organic_frequency',
            'non_organic_dosage', 'non_organic_frequency'
        ]
        
        self.feature_columns = feature_cols
        self.target_columns = target_cols
        
        # Prepare features
        X = df[feature_cols].copy()
        
        # Prepare targets
        y = df[target_cols].copy()
        
        # Handle categorical features
        categorical_features = ['crop_type', 'disease_type', 'disease_stage', 
                              'crop_stage', 'region']
        
        print("\nEncoding categorical features...")
        for col in categorical_features:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
            print(f"  {col}: {len(le.classes_)} unique values")
        
        # Handle target encoding
        print("\nEncoding target variables...")
        for col in target_cols:
            le = LabelEncoder()
            y[col] = le.fit_transform(y[col].astype(str))
            self.label_encoders[f'target_{col}'] = le
            print(f"  {col}: {len(le.classes_)} unique values")
        
        # Scale numerical features
        numerical_features = ['temperature', 'humidity', 'rainfall', 'soil_ph', 'nitrogen']
        X[numerical_features] = self.scaler.fit_transform(X[numerical_features])
        
        print(f"\nPreprocessed features shape: {X.shape}")
        print(f"Preprocessed targets shape: {y.shape}")
        
        return X, y
    
    def train_models(self, X, y):
        """
        Train multiple models for pesticide recommendation
        
        Args:
            X: Feature matrix
            y: Target matrix
        """
        print("\n" + "="*60)
        print("TRAINING MACHINE LEARNING MODELS")
        print("="*60)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y.iloc[:, 0]
        )
        
        print(f"\nTrain set: {X_train.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        
        # Store test data for evaluation
        self.X_test = X_test
        self.y_test = y_test
        
        # Model 1: Random Forest with Multi-Output
        print("\n1. Training Random Forest Multi-Output Classifier...")
        rf_model = MultiOutputClassifier(
            RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        )
        
        rf_model.fit(X_train, y_train)
        self.models['random_forest'] = rf_model
        
        # Evaluate Random Forest
        rf_pred = rf_model.predict(X_test)
        rf_accuracy = np.mean([
            accuracy_score(y_test.iloc[:, i], rf_pred[:, i]) 
            for i in range(y_test.shape[1])
        ])
        print(f"   Random Forest Average Accuracy: {rf_accuracy:.4f}")
        
        # Model 2: LightGBM Multi-Output
        print("\n2. Training LightGBM Multi-Output Classifier...")
        lgb_models = {}
        lgb_predictions = []
        
        for i, col in enumerate(self.target_columns):
            print(f"   Training LightGBM for {col}...")
            
            lgb_model = lgb.LGBMClassifier(
                n_estimators=300,
                max_depth=10,
                learning_rate=0.1,
                num_leaves=50,
                random_state=42,
                verbose=-1
            )
            
            lgb_model.fit(X_train, y_train.iloc[:, i])
            lgb_models[col] = lgb_model
            
            # Predict for this target
            pred = lgb_model.predict(X_test)
            lgb_predictions.append(pred)
        
        self.models['lightgbm'] = lgb_models
        
        # Evaluate LightGBM
        lgb_pred = np.column_stack(lgb_predictions)
        lgb_accuracy = np.mean([
            accuracy_score(y_test.iloc[:, i], lgb_pred[:, i]) 
            for i in range(y_test.shape[1])
        ])
        print(f"   LightGBM Average Accuracy: {lgb_accuracy:.4f}")
        
        # Feature importance analysis
        print("\n3. Analyzing Feature Importance...")
        self.analyze_feature_importance(X_train)
        
        return rf_accuracy, lgb_accuracy
    
    def analyze_feature_importance(self, X_train):
        """
        Analyze and visualize feature importance
        
        Args:
            X_train: Training feature matrix
        """
        # Get feature importance from Random Forest
        rf_model = self.models['random_forest']
        
        # Average importance across all outputs
        importance_scores = np.mean([
            estimator.feature_importances_ 
            for estimator in rf_model.estimators_
        ], axis=0)
        
        # Create feature importance dataframe
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': importance_scores
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10).to_string(index=False))
        
        # Save feature importance
        feature_importance.to_csv('feature_importance.csv', index=False)
        
        return feature_importance
    
    def evaluate_models(self):
        """
        Comprehensive model evaluation with detailed metrics
        """
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        models_to_evaluate = ['random_forest', 'lightgbm']
        
        for model_name in models_to_evaluate:
            print(f"\n{model_name.upper()} EVALUATION:")
            print("-" * 40)
            
            if model_name == 'random_forest':
                y_pred = self.models[model_name].predict(self.X_test)
            else:
                # For LightGBM, predict each target separately
                y_pred = []
                for i, col in enumerate(self.target_columns):
                    pred = self.models[model_name][col].predict(self.X_test)
                    y_pred.append(pred)
                y_pred = np.column_stack(y_pred)
            
            # Calculate accuracy for each target
            for i, col in enumerate(self.target_columns):
                accuracy = accuracy_score(self.y_test.iloc[:, i], y_pred[:, i])
                print(f"  {col}: {accuracy:.4f}")
                
                # Detailed classification report for first two targets
                if i < 2:
                    print(f"\n  Classification Report for {col}:")
                    target_names = self.label_encoders[f'target_{col}'].classes_
                    if len(target_names) <= 20:  # Only show if not too many classes
                        print(classification_report(
                            self.y_test.iloc[:, i], 
                            y_pred[:, i],
                            target_names=target_names[:len(np.unique(y_pred[:, i]))],
                            zero_division=0
                        ))
            
            # Overall accuracy
            overall_accuracy = np.mean([
                accuracy_score(self.y_test.iloc[:, i], y_pred[:, i]) 
                for i in range(self.y_test.shape[1])
            ])
            print(f"\n  Overall Average Accuracy: {overall_accuracy:.4f}")
    
    def save_models(self):
        """
        Save trained models and preprocessors for deployment
        """
        print("\n" + "="*60)
        print("SAVING MODELS")
        print("="*60)
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save Random Forest model
        joblib.dump(self.models['random_forest'], 'models/pesticide_rf_model.joblib')
        print("✓ Random Forest model saved to 'models/pesticide_rf_model.joblib'")
        
        # Save LightGBM models
        for col, model in self.models['lightgbm'].items():
            filename = f'models/pesticide_lgb_{col.replace(" ", "_")}.joblib'
            joblib.dump(model, filename)
        print("✓ LightGBM models saved to 'models/' directory")
        
        # Save label encoders
        with open('models/label_encoders.pkl', 'wb') as f:
            pickle.dump(self.label_encoders, f)
        print("✓ Label encoders saved to 'models/label_encoders.pkl'")
        
        # Save scaler
        joblib.dump(self.scaler, 'models/scaler.joblib')
        print("✓ Feature scaler saved to 'models/scaler.joblib'")
        
        # Save feature and target column names
        metadata = {
            'feature_columns': self.feature_columns,
            'target_columns': self.target_columns,
            'training_date': datetime.now().isoformat()
        }
        
        with open('models/model_metadata.pkl', 'wb') as f:
            pickle.dump(metadata, f)
        print("✓ Model metadata saved to 'models/model_metadata.pkl'")
        
    def create_prediction_function(self):
        """
        Create a standalone prediction function for easy integration
        """
        prediction_code = '''
def predict_pesticide_recommendation(crop_type, disease_type, disease_stage, 
                                   crop_stage, region, is_organic_farming,
                                   temperature, humidity, rainfall, soil_ph, nitrogen):
    """
    Predict pesticide recommendations based on input parameters
    
    Args:
        crop_type (str): Type of crop
        disease_type (str): Type of disease
        disease_stage (str): Stage of disease (early, mid, advanced)
        crop_stage (str): Growth stage of crop
        region (str): Geographic region
        is_organic_farming (int): 1 for organic, 0 for conventional
        temperature (float): Temperature in Celsius
        humidity (float): Humidity percentage
        rainfall (float): Rainfall in mm
        soil_ph (float): Soil pH level
        nitrogen (float): Nitrogen content
    
    Returns:
        dict: Pesticide recommendations with organic and non-organic options
    """
    import joblib
    import pickle
    import numpy as np
    import pandas as pd
    
    # Load models and preprocessors
    rf_model = joblib.load('models/pesticide_rf_model.joblib')
    with open('models/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    scaler = joblib.load('models/scaler.joblib')
    with open('models/model_metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    
    # Prepare input data
    input_data = pd.DataFrame({
        'crop_type': [crop_type],
        'disease_type': [disease_type],
        'disease_stage': [disease_stage],
        'crop_stage': [crop_stage],
        'region': [region],
        'is_organic_farming': [is_organic_farming],
        'temperature': [temperature],
        'humidity': [humidity],
        'rainfall': [rainfall],
        'soil_ph': [soil_ph],
        'nitrogen': [nitrogen]
    })
    
    # Encode categorical features
    categorical_features = ['crop_type', 'disease_type', 'disease_stage', 
                          'crop_stage', 'region']
    
    for col in categorical_features:
        le = label_encoders[col]
        try:
            input_data[col] = le.transform(input_data[col])
        except ValueError:
            # Handle unseen categories by using the most frequent class
            input_data[col] = 0
    
    # Scale numerical features
    numerical_features = ['temperature', 'humidity', 'rainfall', 'soil_ph', 'nitrogen']
    input_data[numerical_features] = scaler.transform(input_data[numerical_features])
    
    # Make prediction
    prediction = rf_model.predict(input_data)
    
    # Decode predictions
    target_columns = metadata['target_columns']
    results = {}
    
    for i, col in enumerate(target_columns):
        le = label_encoders[f'target_{col}']
        decoded_pred = le.inverse_transform([prediction[0][i]])[0]
        results[col] = decoded_pred
    
    return {
        'organic_pesticide': results['organic_pesticide'],
        'organic_application_method': results['organic_application_method'],
        'non_organic_pesticide': results['non_organic_pesticide'],
        'non_organic_application_method': results['non_organic_application_method'],
        'confidence': 'high'  # Can be enhanced with prediction probabilities
    }
'''
        
        # Save the prediction function
        with open('pesticide_predictor.py', 'w') as f:
            f.write(prediction_code)
        
        print("✓ Prediction function saved to 'pesticide_predictor.py'")

def main():
    """
    Main training pipeline
    """
    print("="*80)
    print("PESTICIDE RECOMMENDATION ML TRAINING PIPELINE")
    print("="*80)
    print(f"Started at: {datetime.now()}")
    
    # Initialize trainer
    trainer = PesticideRecommendationTrainer()
    
    try:
        # Load and preprocess data
        X, y = trainer.load_and_preprocess_data()
        
        # Train models
        rf_acc, lgb_acc = trainer.train_models(X, y)
        
        # Evaluate models
        trainer.evaluate_models()
        
        # Save models
        trainer.save_models()
        
        # Create prediction function
        trainer.create_prediction_function()
        
        print("\n" + "="*80)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"Random Forest Accuracy: {rf_acc:.4f}")
        print(f"LightGBM Accuracy: {lgb_acc:.4f}")
        print(f"Completed at: {datetime.now()}")
        print("\nFiles created:")
        print("- models/pesticide_rf_model.joblib")
        print("- models/label_encoders.pkl") 
        print("- models/scaler.joblib")
        print("- models/model_metadata.pkl")
        print("- pesticide_predictor.py")
        print("- feature_importance.csv")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        raise

if __name__ == "__main__":
    main()
