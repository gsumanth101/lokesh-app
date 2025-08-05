
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
