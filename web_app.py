#!/usr/bin/env python3
"""
Smart Farming Web Application
Flask backend for HTML interface and API endpoints
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import sys
from database import DatabaseManager
import pickle
import numpy as np
from datetime import datetime, timedelta
import logging
import requests
import hashlib
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'smart_farming_secret_key_2025'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# --- Configuration ---
OPENCAGE_API_KEY = os.environ.get('OPENCAGE_API_KEY', 'YOUR_OPENCAGE_API_KEY')

# Initialize database
db_manager = DatabaseManager()

# Load models
models = {}
def load_models():
    model_files = {
        'basic': 'crop_recommendation_model.pkl',
        'enhanced': 'enhanced_crop_recommendation_model.pkl',
        'optimized': 'optimized_crop_model.pkl'
    }
    for model_name, filename in model_files.items():
        try:
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    models[model_name] = pickle.load(f)
                logger.info(f"Loaded {model_name} model successfully")
            else:
                logger.warning(f"Model file {filename} not found")
        except Exception as e:
            logger.error(f"Error loading {model_name} model: {e}")

load_models()


# --- Helper Functions for Data Gathering (Moved from app.py) ---

def get_location_coordinates(location: str) -> dict:
    """Get latitude and longitude for a given location using OpenCage Geocoding API."""
    if not OPENCAGE_API_KEY or OPENCAGE_API_KEY == 'YOUR_OPENCAGE_API_KEY':
        logger.error("OpenCage API key is not set.")
        return None
    try:
        url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                geometry = data['results'][0]['geometry']
                return {'lat': geometry['lat'], 'lon': geometry['lng']}
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during geocoding: {e}")
    return None

def get_nasa_weather(lat: float, lon: float) -> dict:
    """Get weather data from NASA Power API."""
    try:
        url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        # Use a recent but reliable date (NASA data has a delay)
        target_date = (datetime.now() - timedelta(days=65)).strftime("%Y%m%d")
        params = {
            'parameters': 'T2M,RH2M,PRECTOTCORR',
            'community': 'AG',
            'longitude': float(lon),
            'latitude': float(lat),
            'start': target_date, 'end': target_date,
            'format': 'JSON'
        }
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                return data
    except Exception as e:
        logger.error(f"Error fetching NASA weather data: {e}")
    return None

def process_nasa_weather(nasa_data: dict) -> dict:
    """Process the raw JSON from NASA Power API into simple values."""
    try:
        params = nasa_data['properties']['parameter']
        temp = list(params['T2M'].values())[0]
        humidity = list(params['RH2M'].values())[0]
        daily_precip = list(params['PRECTOTCORR'].values())[0]
        annual_rainfall = daily_precip * 365 if daily_precip > 0 else 500

        if temp == -999 or humidity == -999: return None
        
        return {'temperature': temp, 'humidity': humidity, 'rainfall': annual_rainfall}
    except Exception as e:
        logger.error(f"Error processing NASA data: {e}")
        return None

def get_simulated_soil(location: str) -> dict:
    """Generates realistic but simulated soil data based on a location name."""
    seed = int(hashlib.md5(location.encode()).hexdigest(), 16)
    random.seed(seed)
    ph = random.uniform(5.5, 7.8)
    organic_matter = random.uniform(1.0, 4.0)
    n = 20 + organic_matter * 20
    p = 25 + organic_matter * 10
    k = 30 + organic_matter * 8
    return {'N': int(n), 'P': int(p), 'K': int(k), 'pH': round(ph, 1)}


# --- API Routes ---

@app.route('/api/login', methods=['POST'])
def api_login():
    # ... (existing login code) ...
    pass

@app.route('/api/register', methods=['POST'])
def api_register():
    # ... (existing register code) ...
    pass

@app.route('/api/logout', methods=['POST'])
def api_logout():
    # ... (existing logout code) ...
    pass

@app.route('/api/crop-recommendation', methods=['POST'])
def api_crop_recommendation():
    """
    API endpoint for crop recommendation.
    Can accept either a full feature set or just a location name.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Invalid input'}), 400

        location = data.get('location')
        features_manual = data.get('features')
        model_type = data.get('model', 'basic')
        
        if not location and not features_manual:
            return jsonify({'success': False, 'message': 'Either location or features are required'}), 400

        if location:
            # --- This is the new logic for IVR and location-based requests ---
            logger.info(f"API: Received request for location: {location}")
            coords = get_location_coordinates(location)
            if not coords:
                return jsonify({'success': False, 'message': f"Could not find coordinates for {location}."})

            nasa_raw = get_nasa_weather(coords['lat'], coords['lon'])
            if not nasa_raw:
                return jsonify({'success': False, 'message': "Failed to retrieve weather data."})

            weather = process_nasa_weather(nasa_raw)
            if not weather:
                return jsonify({'success': False, 'message': "Failed to process weather data."})
                
            soil = get_simulated_soil(location)

            features = [
                soil['N'], soil['P'], soil['K'],
                weather['temperature'], weather['humidity'],
                soil['pH'], weather['rainfall']
            ]
        else:
            # --- This is the existing logic for feature-based requests ---
            logger.info("API: Received request with manual features.")
            features = features_manual
        
        # --- Prediction Step (common for both paths) ---
        model = models.get(model_type, models['basic'])
        features_array = np.array([features])
        prediction = model.predict(features_array)[0]
        confidence = model.predict_proba(features_array).max() * 100 if hasattr(model, 'predict_proba') else None

        response_data = {
            'recommended_crop': prediction,
            'confidence': f"{confidence:.2f}%" if confidence else "N/A",
            'model_used': model_type
        }
        return jsonify({'success': True, 'data': response_data})

    except Exception as e:
        logger.error(f"Crop recommendation error: {e}")
        return jsonify({'success': False, 'message': 'Prediction failed'}), 500

@app.route('/api/market-prices')
def api_market_prices():
    # ... (existing market prices code) ...
    pass

# ... (Add other existing API routes like /api/listings, etc.) ...

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': list(models.keys())
    })

if __name__ == '__main__':
    print("🌾 Starting Smart Farming Web Application")
    print("=" * 50)
    print(f"🔧 Models loaded: {list(models.keys())}")
    print(f"🌐 Starting server on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

    # In web_app.py

from app import predict_disease # Import the advanced function from your main app file

@app.route('/api/predict-disease', methods=['POST'])
def api_predict_disease():
    """API endpoint for the advanced, rule-based disease prediction."""
    try:
        data = request.get_json()
        if not data or 'crop_name' not in data:
            return jsonify({'success': False, 'message': 'Crop name is required.'}), 400
        
        # Use default weather values, as the IVR won't collect this level of detail
        weather_defaults = {
            'temperature': 28.0, 'humidity': 75, 'rainfall': 900,
            'wind_speed': 5.0, 'specific_humidity': 0.01, 'ph': 6.5
        }
        
        result = predict_disease(
            crop_name=data['crop_name'],
            temperature=float(data.get('temperature', weather_defaults['temperature'])),
            humidity=float(data.get('humidity', weather_defaults['humidity'])),
            rainfall=float(data.get('rainfall', weather_defaults['rainfall'])),
            wind_speed=float(data.get('wind_speed', weather_defaults['wind_speed'])),
            specific_humidity=float(data.get('specific_humidity', weather_defaults['specific_humidity'])),
            ph=float(data.get('ph', weather_defaults['ph']))
        )
        
        logger.info(f"Disease prediction for {data['crop_name']}: {result.get('primary_disease')}")
        
        return jsonify({'success': True, 'data': result})
        
    except Exception as e:
        logger.error(f"Disease prediction API error: {e}")
        return jsonify({'success': False, 'message': 'Disease prediction failed'}), 500