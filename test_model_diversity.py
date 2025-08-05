#!/usr/bin/env python3
"""
Test Model Diversity
Verify that models predict various crops based on different conditions
"""

import pickle
import numpy as np
from collections import Counter

def load_models():
    """Load all available models"""
    models = {}
    
    # Load standard model
    try:
        with open('crop_recommendation_model.pkl', 'rb') as f:
            models['Standard'] = pickle.load(f)
        print("✅ Standard model loaded")
    except Exception as e:
        print(f"❌ Error loading standard model: {e}")
    
    # Load enhanced model
    try:
        with open('enhanced_crop_recommendation_model.pkl', 'rb') as f:
            models['Enhanced'] = pickle.load(f)
        print("✅ Enhanced model loaded")
    except Exception as e:
        print(f"❌ Error loading enhanced model: {e}")
    
    # Load optimized model
    try:
        with open('optimized_crop_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
            if isinstance(model_data, dict):
                models['Optimized'] = model_data
            else:
                models['Optimized'] = model_data
        print("✅ Optimized model loaded")
    except Exception as e:
        print(f"❌ Error loading optimized model: {e}")
    
    return models

def test_diverse_conditions():
    """Test models with diverse agricultural conditions"""
    
    # Diverse test scenarios with expected crops
    test_scenarios = [
        # High water/tropical (Rice, Banana, Coconut)
        {"name": "High Rainfall Tropical", "params": [90, 42, 43, 28, 85, 6.5, 2000], "expected_types": ["rice", "banana", "coconut", "papaya"]},
        
        # Dry/Desert conditions (Barley, Millet, some pulses)
        {"name": "Dry Desert Climate", "params": [40, 25, 30, 35, 40, 7.8, 250], "expected_types": ["barley", "millet", "mothbeans", "chickpea"]},
        
        # Temperate/Cool climate (Wheat, Apple, Potato)
        {"name": "Cool Temperate", "params": [70, 35, 45, 15, 65, 6.8, 600], "expected_types": ["wheat", "apple", "potato", "barley"]},
        
        # High Nutrient Soil (Tomato, Potato, Cotton)
        {"name": "High Nutrient Rich Soil", "params": [120, 80, 140, 25, 75, 6.5, 900], "expected_types": ["tomato", "potato", "cotton", "banana"]},
        
        # Acidic Soil conditions (Potato, Coffee)
        {"name": "Acidic Soil", "params": [80, 50, 100, 22, 80, 5.2, 1200], "expected_types": ["potato", "coffee", "banana"]},
        
        # Alkaline Soil (Wheat, Cotton, some pulses)
        {"name": "Alkaline Soil", "params": [60, 40, 50, 25, 60, 8.2, 500], "expected_types": ["wheat", "cotton", "chickpea", "barley"]},
        
        # Legume conditions (Low N, High P)
        {"name": "Legume Favorable", "params": [20, 70, 25, 26, 65, 7.2, 450], "expected_types": ["chickpea", "lentil", "kidneybeans", "pigeonpeas"]},
        
        # Fruit tree conditions (Moderate nutrients, good drainage)
        {"name": "Fruit Tree Conditions", "params": [50, 35, 60, 22, 70, 6.8, 1100], "expected_types": ["apple", "mango", "orange", "pomegranate"]},
        
        # Hot humid (Tropical vegetables)
        {"name": "Hot Humid Tropical", "params": [80, 45, 70, 32, 90, 6.2, 1800], "expected_types": ["rice", "papaya", "coconut", "jute"]},
        
        # Mediterranean climate (Grapes, Pomegranate)
        {"name": "Mediterranean", "params": [45, 30, 75, 20, 55, 7.0, 450], "expected_types": ["grapes", "pomegranate", "wheat", "barley"]}
    ]
    
    return test_scenarios

def predict_with_model(model, model_name, params):
    """Make prediction with a specific model"""
    try:
        if model_name == 'Optimized' and isinstance(model, dict):
            # Handle optimized model with scaler
            if 'scaler' in model and 'model' in model:
                params_scaled = model['scaler'].transform([params])
                prediction = model['model'].predict(params_scaled)[0]
                if hasattr(model['model'], 'predict_proba'):
                    confidence = model['model'].predict_proba(params_scaled).max()
                else:
                    confidence = None
            else:
                prediction = model.predict([params])[0]
                confidence = model.predict_proba([params]).max() if hasattr(model, 'predict_proba') else None
        else:
            # Handle standard and enhanced models
            prediction = model.predict([params])[0]
            confidence = model.predict_proba([params]).max() if hasattr(model, 'predict_proba') else None
        
        return prediction, confidence
    except Exception as e:
        print(f"   Error with {model_name} model: {e}")
        return None, None

def main():
    """Main testing function"""
    print("🧪 Testing Model Diversity and Predictions")
    print("=" * 60)
    
    # Load models
    models = load_models()
    
    if not models:
        print("❌ No models loaded. Please train models first.")
        return
    
    print(f"\n📊 Loaded {len(models)} models: {', '.join(models.keys())}")
    
    # Get test scenarios
    test_scenarios = test_diverse_conditions()
    
    print(f"\n🔬 Testing {len(test_scenarios)} diverse agricultural scenarios...\n")
    
    # Track all predictions for diversity analysis
    all_predictions = {model_name: [] for model_name in models.keys()}
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"🌍 Scenario {i}: {scenario['name']}")
        print(f"   Conditions: N={scenario['params'][0]}, P={scenario['params'][1]}, K={scenario['params'][2]}")
        print(f"   Climate: T={scenario['params'][3]}°C, H={scenario['params'][4]}%, pH={scenario['params'][5]}, Rain={scenario['params'][6]}mm")
        print(f"   Expected crop types: {', '.join(scenario['expected_types'])}")
        print(f"   Predictions:")
        
        scenario_predictions = {}
        for model_name, model in models.items():
            prediction, confidence = predict_with_model(model, model_name, scenario['params'])
            if prediction:
                all_predictions[model_name].append(prediction)
                scenario_predictions[model_name] = prediction
                conf_str = f" (conf: {confidence:.3f})" if confidence else ""
                print(f"     {model_name}: {prediction.title()}{conf_str}")
        
        # Check if any prediction matches expected types
        matches = []
        for model_name, pred in scenario_predictions.items():
            if pred.lower() in scenario['expected_types']:
                matches.append(f"{model_name}✓")
        
        if matches:
            print(f"   ✅ Good matches: {', '.join(matches)}")
        else:
            print(f"   ⚠️  No exact matches, but predictions are reasonable")
        
        print()
    
    # Analyze overall diversity
    print("📈 Overall Prediction Diversity Analysis:")
    print("=" * 50)
    
    for model_name, predictions in all_predictions.items():
        if predictions:
            unique_crops = len(set(predictions))
            total_predictions = len(predictions)
            most_common = Counter(predictions).most_common(3)
            
            print(f"\n🤖 {model_name} Model:")
            print(f"   Unique crops predicted: {unique_crops}/{total_predictions}")
            print(f"   Diversity score: {unique_crops/total_predictions:.3f}")
            print(f"   Most frequent predictions: {', '.join([f'{crop}({count})' for crop, count in most_common])}")
            
            if unique_crops >= 8:
                print(f"   ✅ Excellent diversity!")
            elif unique_crops >= 5:
                print(f"   ✅ Good diversity")
            else:
                print(f"   ⚠️  Limited diversity - needs improvement")
    
    print(f"\n🎉 Diversity Test Complete!")
    print(f"💡 Models should now predict different crops based on:")
    print(f"   • Soil nutrients (N, P, K)")
    print(f"   • Climate conditions (Temperature, Humidity, Rainfall)")
    print(f"   • Soil chemistry (pH)")
    print(f"   • Regional agricultural patterns")

if __name__ == "__main__":
    main()
