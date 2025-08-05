import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load dataset
data = pd.read_csv('data/pesticide_recommendation_training_dataset.csv')

# Preprocess dataset
categorical_features = ['crop_type', 'disease_type', 'disease_stage', 'crop_stage', 'region']
numerical_features = ['temperature', 'humidity', 'rainfall', 'soil_ph', 'nitrogen']

# Handle categorical features with Label Encoding (more efficient for tree-based models)
label_encoders = {}
for feature in categorical_features:
    le = LabelEncoder()
    data[feature + '_encoded'] = le.fit_transform(data[feature])
    label_encoders[feature] = le

# Normalize numerical features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(data[numerical_features])
scaled_df = pd.DataFrame(scaled_features, columns=numerical_features)

# Combine features
encoded_cat_features = [f + '_encoded' for f in categorical_features] + ['is_organic_farming']
X = pd.concat([data[encoded_cat_features], scaled_df], axis=1)

# Encode target variables
organic_encoder = LabelEncoder()
y_organic = organic_encoder.fit_transform(data['organic_pesticide'])

non_organic_encoder = LabelEncoder()
y_non_organic = non_organic_encoder.fit_transform(data['non_organic_pesticide'])

# Split dataset
X_train, X_test, y_organic_train, y_organic_test = train_test_split(X, y_organic, test_size=0.2, random_state=42)
_, _, y_non_organic_train, y_non_organic_test = train_test_split(X, y_non_organic, test_size=0.2, random_state=42)

# Train separate models for organic and non-organic pesticides
organic_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
organic_model.fit(X_train, y_organic_train)

non_organic_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
non_organic_model.fit(X_train, y_non_organic_train)

# Predict and evaluate
organic_train_preds = organic_model.predict(X_train)
organic_test_preds = organic_model.predict(X_test)

non_organic_train_preds = non_organic_model.predict(X_train)
non_organic_test_preds = non_organic_model.predict(X_test)

# Calculate metrics
organic_train_accuracy = accuracy_score(y_organic_train, organic_train_preds)
organic_test_accuracy = accuracy_score(y_organic_test, organic_test_preds)
organic_train_f1 = f1_score(y_organic_train, organic_train_preds, average='weighted')
organic_test_f1 = f1_score(y_organic_test, organic_test_preds, average='weighted')

non_organic_train_accuracy = accuracy_score(y_non_organic_train, non_organic_train_preds)
non_organic_test_accuracy = accuracy_score(y_non_organic_test, non_organic_test_preds)
non_organic_train_f1 = f1_score(y_non_organic_train, non_organic_train_preds, average='weighted')
non_organic_test_f1 = f1_score(y_non_organic_test, non_organic_test_preds, average='weighted')

print("\n=== Organic Pesticide Model Performance ===")
print(f"Train Accuracy: {organic_train_accuracy:.3f}")
print(f"Test Accuracy: {organic_test_accuracy:.3f}")
print(f"Train F1 Score: {organic_train_f1:.3f}")
print(f"Test F1 Score: {organic_test_f1:.3f}")

print("\n=== Non-Organic Pesticide Model Performance ===")
print(f"Train Accuracy: {non_organic_train_accuracy:.3f}")
print(f"Test Accuracy: {non_organic_test_accuracy:.3f}")
print(f"Train F1 Score: {non_organic_train_f1:.3f}")
print(f"Test F1 Score: {non_organic_test_f1:.3f}")

# Save models and encoders
model_data = {
    'organic_model': organic_model,
    'non_organic_model': non_organic_model,
    'label_encoders': label_encoders,
    'scaler': scaler,
    'organic_encoder': organic_encoder,
    'non_organic_encoder': non_organic_encoder
}
joblib.dump(model_data, 'pesticide_model.pkl')

print("\n=== Testing with Sample Prediction ===")

# Function to predict pesticides for new input
def predict_pesticides(crop_type, disease_type, disease_stage, crop_stage, region, is_organic_farming, temperature, humidity, rainfall, soil_ph, nitrogen):
    # Load the saved model
    model_data = joblib.load('pesticide_model.pkl')
    
    # Create input dataframe
    input_data = pd.DataFrame([{
        'crop_type': crop_type,
        'disease_type': disease_type,
        'disease_stage': disease_stage,
        'crop_stage': crop_stage,
        'region': region,
        'is_organic_farming': is_organic_farming,
        'temperature': temperature,
        'humidity': humidity,
        'rainfall': rainfall,
        'soil_ph': soil_ph,
        'nitrogen': nitrogen
    }])
    
    # Encode categorical features
    for feature in categorical_features:
        if feature in model_data['label_encoders']:
            try:
                input_data[feature + '_encoded'] = model_data['label_encoders'][feature].transform([input_data[feature].iloc[0]])
            except ValueError:
                # Handle unseen categories
                input_data[feature + '_encoded'] = 0
    
    # Scale numerical features
    scaled_features = model_data['scaler'].transform(input_data[numerical_features])
    scaled_df = pd.DataFrame(scaled_features, columns=numerical_features)
    
    # Combine features
    encoded_cat_features = [f + '_encoded' for f in categorical_features] + ['is_organic_farming']
    X_new = pd.concat([input_data[encoded_cat_features], scaled_df], axis=1)
    
    # Predict
    organic_pred = model_data['organic_model'].predict(X_new)[0]
    non_organic_pred = model_data['non_organic_model'].predict(X_new)[0]
    
    # Decode predictions
    organic_pesticide = model_data['organic_encoder'].inverse_transform([organic_pred])[0]
    non_organic_pesticide = model_data['non_organic_encoder'].inverse_transform([non_organic_pred])[0]
    
    return organic_pesticide, non_organic_pesticide

# Test with sample data
sample_organic, sample_non_organic = predict_pesticides(
    crop_type='rice',
    disease_type='leaf blight',
    disease_stage='mid',
    crop_stage='flowering',
    region='Tamil Nadu',
    is_organic_farming=1,
    temperature=26.5,
    humidity=75,
    rainfall=10,
    soil_ph=6.5,
    nitrogen=70
)

print(f"Recommended Organic Pesticide: {sample_organic}")
print(f"Recommended Non-Organic Pesticide: {sample_non_organic}")
print("\nModel training and testing completed successfully!")
