import pickle

try:
    with open('optimized_crop_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    print("Model data keys:", list(model_data.keys()))
    
    for key, value in model_data.items():
        if key == 'model':
            print(f"{key}: {type(value)}")
        elif key == 'feature_names':
            print(f"{key}: {value}")
        elif key == 'feature_importance':
            print(f"{key}: DataFrame with shape {value.shape}")
        else:
            print(f"{key}: {value}")
            
except Exception as e:
    print(f"Error loading model: {e}")
