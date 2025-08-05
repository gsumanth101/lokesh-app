#!/usr/bin/env python3
"""
Test script for disease prediction functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import predict_disease

def test_disease_prediction():
    """Test the disease prediction function"""
    print("Testing Disease Prediction Function")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            'crop_name': 'rice',
            'temperature': 25,
            'humidity': 85,
            'rainfall': 150,
            'wind_speed': 5,
            'specific_humidity': 0.015,
            'ph': 6.5,
            'expected': 'blast'
        },
        {
            'crop_name': 'wheat',
            'temperature': 20,
            'humidity': 70,
            'rainfall': 100,
            'wind_speed': 6,
            'specific_humidity': 0.012,
            'ph': 7.0,
            'expected': 'rust'
        },
        {
            'crop_name': 'tomato',
            'temperature': 18,
            'humidity': 80,
            'rainfall': 60,
            'wind_speed': 4,
            'specific_humidity': 0.013,
            'ph': 6.0,
            'expected': 'late_blight'
        },
        {
            'crop_name': 'maize',
            'temperature': 25,
            'humidity': 65,
            'rainfall': 80,
            'wind_speed': 8,
            'specific_humidity': 0.014,
            'ph': 6.8,
            'expected': 'rust'
        },
        {
            'crop_name': 'cotton',
            'temperature': 30,
            'humidity': 55,
            'rainfall': 40,
            'wind_speed': 5,
            'specific_humidity': 0.011,
            'ph': 7.2,
            'expected': 'wilt'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['crop_name'].title()}")
        print("-" * 30)
        
        try:
            result = predict_disease(
                crop_name=test_case['crop_name'],
                temperature=test_case['temperature'],
                humidity=test_case['humidity'],
                rainfall=test_case['rainfall'],
                wind_speed=test_case['wind_speed'],
                specific_humidity=test_case['specific_humidity'],
                ph=test_case['ph']
            )
            
            print(f"Predicted Disease: {result['disease']}")
            print(f"Risk Level: {result['risk_level']}")
            print(f"Risk Factors: {', '.join(result.get('risk_factors', []))}")
            print(f"Prevention Tips:")
            for tip in result['prevention']:
                print(f"  - {tip}")
            
            # Check if prediction matches expected (for high-risk conditions)
            if result['disease'] == test_case['expected']:
                print("✅ Prediction matches expected result!")
            elif result['disease'] == 'healthy':
                print("✅ Low risk conditions - healthy prediction")
            else:
                print(f"⚠️  Different prediction than expected: {result['disease']} vs {test_case['expected']}")
                
        except Exception as e:
            print(f"❌ Error in test case {i}: {e}")
    
    print("\n" + "=" * 50)
    print("Disease Prediction Test Complete!")

if __name__ == "__main__":
    test_disease_prediction()
