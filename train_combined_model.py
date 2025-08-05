import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

def load_and_combine_datasets():
    """Load and combine the two datasets"""
    print("Loading datasets...")
    
    # Load the first dataset (Crop_recommendationV2.csv)
    try:
        crop_v2 = pd.read_csv('C:/Users/navya/Downloads/Crop_recommendationV2.csv')
        print(f"Loaded Crop_recommendationV2.csv: {crop_v2.shape}")
    except Exception as e:
        print(f"Error loading Crop_recommendationV2.csv: {e}")
        return None
    
    # Load the second dataset (enhanced_crop_data.csv)
    try:
        enhanced_crop = pd.read_csv('data/enhanced_crop_data.csv')
        print(f"Loaded enhanced_crop_data.csv: {enhanced_crop.shape}")
    except Exception as e:
        print(f"Error loading enhanced_crop_data.csv: {e}")
        return None
    
    # Standardize column names for crop_v2
    if 'label' in crop_v2.columns:
        crop_v2 = crop_v2.rename(columns={'label': 'crop'})
    
    # Select common features from both datasets
    common_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    # Rename 'ph' to 'pH' for consistency if needed
    if 'ph' in crop_v2.columns:
        crop_v2 = crop_v2.rename(columns={'ph': 'pH'})
    if 'ph' in enhanced_crop.columns:
        enhanced_crop = enhanced_crop.rename(columns={'ph': 'pH'})
    
    # Update common features
    common_features = ['N', 'P', 'K', 'temperature', 'humidity', 'pH', 'rainfall', 'crop']
    
    # Select only common features from both datasets
    crop_v2_filtered = crop_v2[common_features].copy()
    enhanced_crop_filtered = enhanced_crop[common_features].copy()
    
    # Combine datasets
    combined_data = pd.concat([crop_v2_filtered, enhanced_crop_filtered], ignore_index=True)
    
    # Remove duplicates
    combined_data = combined_data.drop_duplicates()
    
    print(f"Combined dataset shape: {combined_data.shape}")
    print(f"Crops in combined dataset: {combined_data['crop'].unique()}")
    
    return combined_data

def add_cultivation_timing_data(df):
    """Add cultivation timing and duration data to the dataset"""
    print("Adding cultivation timing and duration data...")
    
    # Define cultivation data for different crops
    cultivation_data = {
        'rice': {
            'best_season': 'Monsoon/Summer',
            'planting_months': 'June-July (Kharif), November-December (Rabi)',
            'cultivation_duration': 120,  # days
            'harvest_months': 'October-November (Kharif), March-April (Rabi)',
            'water_requirement': 'High'
        },
        'wheat': {
            'best_season': 'Winter',
            'planting_months': 'November-December',
            'cultivation_duration': 120,  # days
            'harvest_months': 'March-April',
            'water_requirement': 'Medium'
        },
        'maize': {
            'best_season': 'Summer/Monsoon',
            'planting_months': 'June-July (Monsoon), February-March (Summer)',
            'cultivation_duration': 90,  # days
            'harvest_months': 'September-October (Monsoon), May-June (Summer)',
            'water_requirement': 'Medium'
        },
        'cotton': {
            'best_season': 'Summer',
            'planting_months': 'April-June',
            'cultivation_duration': 180,  # days
            'harvest_months': 'October-December',
            'water_requirement': 'High'
        },
        'sugarcane': {
            'best_season': 'Year-round',
            'planting_months': 'February-March, October-November',
            'cultivation_duration': 365,  # days (12 months)
            'harvest_months': 'December-March',
            'water_requirement': 'Very High'
        },
        'tomato': {
            'best_season': 'Winter/Summer',
            'planting_months': 'September-October (Winter), February-March (Summer)',
            'cultivation_duration': 90,  # days
            'harvest_months': 'December-January (Winter), May-June (Summer)',
            'water_requirement': 'Medium'
        },
        'potato': {
            'best_season': 'Winter',
            'planting_months': 'October-November',
            'cultivation_duration': 90,  # days
            'harvest_months': 'January-February',
            'water_requirement': 'Medium'
        },
        'onion': {
            'best_season': 'Winter/Summer',
            'planting_months': 'November-December (Winter), February-March (Summer)',
            'cultivation_duration': 120,  # days
            'harvest_months': 'March-April (Winter), June-July (Summer)',
            'water_requirement': 'Low-Medium'
        },
        'barley': {
            'best_season': 'Winter',
            'planting_months': 'October-November',
            'cultivation_duration': 120,  # days
            'harvest_months': 'February-March',
            'water_requirement': 'Low'
        },
        'millet': {
            'best_season': 'Monsoon',
            'planting_months': 'June-July',
            'cultivation_duration': 75,  # days
            'harvest_months': 'September-October',
            'water_requirement': 'Very Low'
        }
    }
    
    # Add cultivation data to dataframe
    df['best_season'] = df['crop'].map(lambda x: cultivation_data.get(x, {}).get('best_season', 'Unknown'))
    df['planting_months'] = df['crop'].map(lambda x: cultivation_data.get(x, {}).get('planting_months', 'Unknown'))
    df['cultivation_duration'] = df['crop'].map(lambda x: cultivation_data.get(x, {}).get('cultivation_duration', 90))
    df['harvest_months'] = df['crop'].map(lambda x: cultivation_data.get(x, {}).get('harvest_months', 'Unknown'))
    df['water_requirement'] = df['crop'].map(lambda x: cultivation_data.get(x, {}).get('water_requirement', 'Medium'))
    
    return df

def train_enhanced_model():
    """Train enhanced model with combined datasets and cultivation timing"""
    
    # Load and combine datasets
    combined_data = load_and_combine_datasets()
    if combined_data is None:
        print("Failed to load datasets. Exiting...")
        return
    
    # Add cultivation timing data
    combined_data = add_cultivation_timing_data(combined_data)
    
    # Save the enhanced dataset
    combined_data.to_csv('data/combined_enhanced_crop_data.csv', index=False)
    print("Enhanced combined dataset saved to data/combined_enhanced_crop_data.csv")
    
    # Prepare features for training
    feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'pH', 'rainfall']
    X = combined_data[feature_columns]
    y = combined_data['crop']
    
    print(f"Training data shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train Random Forest model
    print("\nTraining Random Forest model...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    
    # Evaluate Random Forest
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    print(f"Random Forest Accuracy: {rf_accuracy:.4f}")
    
    # Train Gradient Boosting model
    print("\nTraining Gradient Boosting model...")
    gb_model = GradientBoostingClassifier(
        n_estimators=150,
        max_depth=10,
        learning_rate=0.1,
        random_state=42
    )
    gb_model.fit(X_train, y_train)
    
    # Evaluate Gradient Boosting
    gb_pred = gb_model.predict(X_test)
    gb_accuracy = accuracy_score(y_test, gb_pred)
    print(f"Gradient Boosting Accuracy: {gb_accuracy:.4f}")
    
    # Select best model
    if rf_accuracy >= gb_accuracy:
        best_model = rf_model
        best_name = "Random Forest"
        best_accuracy = rf_accuracy
    else:
        best_model = gb_model
        best_name = "Gradient Boosting"
        best_accuracy = gb_accuracy
    
    print(f"\nBest model: {best_name} with accuracy: {best_accuracy:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Save the best model
    model_data = {
        'model': best_model,
        'feature_columns': feature_columns,
        'model_name': best_name,
        'accuracy': best_accuracy,
        'cultivation_data': combined_data[['crop', 'best_season', 'planting_months', 
                                        'cultivation_duration', 'harvest_months', 'water_requirement']].drop_duplicates()
    }
    
    with open('enhanced_crop_recommendation_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\nEnhanced model saved as 'enhanced_crop_recommendation_model.pkl'")
    
    # Print classification report
    print(f"\nClassification Report for {best_name}:")
    if best_name == "Random Forest":
        print(classification_report(y_test, rf_pred))
    else:
        print(classification_report(y_test, gb_pred))
    
    return best_model, model_data

if __name__ == "__main__":
    print("Training Enhanced Crop Recommendation Model with Combined Datasets...")
    print("=" * 70)
    
    model, model_data = train_enhanced_model()
    
    print("\n" + "=" * 70)
    print("Training completed successfully!")
    print("Enhanced model with cultivation timing data is ready for use.")
