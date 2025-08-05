import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load the enhanced crop recommendation dataset"""
    print("Loading Crop_recommendationV2.csv dataset...")
    
    # Load the dataset
    df = pd.read_csv('C:\\Users\\navya\\Downloads\\Crop_recommendationV2.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Features: {df.columns.tolist()}")
    print(f"Unique crops: {df['label'].unique()}")
    
    # Check for missing values
    print(f"Missing values: {df.isnull().sum().sum()}")
    
    # Basic statistics
    print("\nDataset Info:")
    print(df.info())
    
    return df

def preprocess_data(df):
    """Preprocess the data for training"""
    
    # Separate features and target
    feature_columns = [col for col in df.columns if col != 'label']
    X = df[feature_columns]
    y = df['label']
    
    print(f"Features: {feature_columns}")
    print(f"Number of features: {len(feature_columns)}")
    print(f"Target distribution:")
    print(y.value_counts())
    
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Convert back to DataFrame to maintain column names
    X_scaled = pd.DataFrame(X_scaled, columns=feature_columns)
    
    return X_scaled, y, scaler, feature_columns

def train_model(X, y):
    """Train the Random Forest model"""
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Feature Importances:")
    print(feature_importance.head(10))
    
    return model, accuracy, feature_importance

def save_model(model, scaler, feature_columns, accuracy):
    """Save the trained model and preprocessing components"""
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'accuracy': accuracy
    }
    
    # Save the complete model
    with open('enhanced_crop_recommendation_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"Model saved as 'enhanced_crop_recommendation_model.pkl'")
    print(f"Model accuracy: {accuracy:.4f}")

def main():
    """Main training function"""
    
    print("=" * 50)
    print("ENHANCED CROP RECOMMENDATION MODEL TRAINING")
    print("=" * 50)
    
    try:
        # Load data
        df = load_and_prepare_data()
        
        # Preprocess data
        X, y, scaler, feature_columns = preprocess_data(df)
        
        # Train model
        model, accuracy, feature_importance = train_model(X, y)
        
        # Save model
        save_model(model, scaler, feature_columns, accuracy)
        
        print("\n" + "=" * 50)
        print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
        return model, scaler, feature_columns
        
    except Exception as e:
        print(f"Error during training: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

if __name__ == "__main__":
    main()
