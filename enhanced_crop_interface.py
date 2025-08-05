import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

# Load the enhanced model
@st.cache_resource
def load_enhanced_model():
    """Load the enhanced crop recommendation model"""
    try:
        with open('enhanced_crop_recommendation_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        return model_data
    except FileNotFoundError:
        st.error("Enhanced model not found. Please run train_new_model.py first.")
        return None

def show_enhanced_crop_interface():
    """Display the enhanced crop recommendation interface"""
    
    st.title("🌾 Enhanced Crop Recommendation System")
    st.markdown("""
    ### 🚀 Advanced AI-Powered Crop Recommendation
    This enhanced system uses **22 environmental and soil parameters** to provide highly accurate crop recommendations.
    
    **Model Performance:**
    - **Accuracy:** 99.55%
    - **Crops Supported:** 22 different crops
    - **Features:** 22 comprehensive parameters
    """)
    
    # Load the model
    model_data = load_enhanced_model()
    if model_data is None:
        return
    
    model = model_data['model']
    scaler = model_data['scaler']
    feature_columns = model_data['feature_columns']
    accuracy = model_data['accuracy']
    
    st.success(f"✅ Enhanced Model Loaded Successfully! (Accuracy: {accuracy:.2%})")
    
    st.markdown("---")
    
    # Create input interface
    st.subheader("🌱 Enter Crop Parameters")
    
    # Primary soil nutrients
    st.markdown("**🧪 Primary Soil Nutrients (NPK)**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50, step=1,
                           help="Nitrogen content in soil (mg/kg)")
    
    with col2:
        P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50, step=1,
                           help="Phosphorus content in soil (mg/kg)")
    
    with col3:
        K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50, step=1,
                           help="Potassium content in soil (mg/kg)")
    
    # Weather and climate parameters
    st.markdown("**🌤️ Weather & Climate Parameters**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0, step=0.1,
                                     help="Average temperature in Celsius")
    
    with col2:
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0,
                                  help="Relative humidity percentage")
    
    with col3:
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=3000.0, value=200.0, step=10.0,
                                  help="Annual rainfall in millimeters")
    
    with col4:
        ph = st.number_input("pH Level", min_value=3.0, max_value=10.0, value=6.5, step=0.1,
                            help="Soil pH level")
    
    # Soil characteristics
    st.markdown("**🌱 Soil Characteristics**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0,
                                       help="Current soil moisture percentage")
    
    with col2:
        soil_type = st.selectbox("Soil Type", options=[1, 2, 3], 
                                format_func=lambda x: ["Sandy", "Loamy", "Clay"][x-1], index=1,
                                help="Primary soil type")
    
    with col3:
        organic_matter = st.number_input("Organic Matter (%)", min_value=0.0, max_value=15.0, value=3.0, step=0.1,
                                        help="Organic matter content in soil")
    
    with col4:
        sunlight_exposure = st.number_input("Sunlight Exposure (hours)", min_value=0.0, max_value=24.0, value=8.0, step=0.1,
                                           help="Daily sunlight exposure hours")
    
    # Environmental factors
    st.markdown("**🌍 Environmental Factors**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=50.0, value=5.0, step=0.1,
                                    help="Average wind speed")
    
    with col2:
        co2_concentration = st.number_input("CO2 Concentration (ppm)", min_value=300.0, max_value=500.0, value=400.0, step=1.0,
                                           help="Atmospheric CO2 concentration")
    
    with col3:
        frost_risk = st.number_input("Frost Risk", min_value=0.0, max_value=100.0, value=20.0, step=1.0,
                                    help="Frost risk level (0-100)")
    
    with col4:
        water_usage_efficiency = st.number_input("Water Usage Efficiency", min_value=0.5, max_value=5.0, value=2.0, step=0.1,
                                                help="Water usage efficiency rating")
    
    # Agricultural management
    st.markdown("**🚜 Agricultural Management**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        irrigation_frequency = st.number_input("Irrigation Frequency", min_value=1, max_value=10, value=3, step=1,
                                              help="Weekly irrigation frequency")
    
    with col2:
        crop_density = st.number_input("Crop Density", min_value=1.0, max_value=50.0, value=10.0, step=0.1,
                                      help="Crop density per square meter")
    
    with col3:
        pest_pressure = st.number_input("Pest Pressure", min_value=0.0, max_value=100.0, value=20.0, step=1.0,
                                       help="Pest pressure level (0-100)")
    
    with col4:
        fertilizer_usage = st.number_input("Fertilizer Usage (kg/ha)", min_value=0.0, max_value=500.0, value=100.0, step=1.0,
                                          help="Fertilizer usage in kg per hectare")
    
    # Additional factors
    st.markdown("**📍 Additional Factors**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        growth_stage = st.selectbox("Growth Stage", options=[1, 2, 3, 4, 5], 
                                   format_func=lambda x: ["Seedling", "Vegetative", "Flowering", "Fruiting", "Harvest"][x-1], 
                                   index=1, help="Current growth stage")
    
    with col2:
        urban_area_proximity = st.number_input("Urban Area Proximity (km)", min_value=0.0, max_value=100.0, value=25.0, step=1.0,
                                              help="Distance to nearest urban area")
    
    with col3:
        water_source_type = st.selectbox("Water Source Type", options=[1, 2, 3], 
                                        format_func=lambda x: ["Surface Water", "Groundwater", "Rainwater"][x-1], 
                                        index=1, help="Primary water source type")
    
    # Prediction button
    st.markdown("---")
    if st.button("🌾 Get Crop Recommendation", type="primary"):
        
        # Prepare input data
        input_data = {
            'N': N,
            'P': P,
            'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall,
            'soil_moisture': soil_moisture,
            'soil_type': soil_type,
            'sunlight_exposure': sunlight_exposure,
            'wind_speed': wind_speed,
            'co2_concentration': co2_concentration,
            'organic_matter': organic_matter,
            'irrigation_frequency': irrigation_frequency,
            'crop_density': crop_density,
            'pest_pressure': pest_pressure,
            'fertilizer_usage': fertilizer_usage,
            'growth_stage': growth_stage,
            'urban_area_proximity': urban_area_proximity,
            'water_source_type': water_source_type,
            'frost_risk': frost_risk,
            'water_usage_efficiency': water_usage_efficiency
        }
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Reorder columns to match training data
        input_df = input_df[feature_columns]
        
        # Scale the input data
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        prediction_proba = model.predict_proba(input_scaled)[0]
        confidence = max(prediction_proba) * 100
        
        # Get top 3 predictions
        classes = model.classes_
        proba_df = pd.DataFrame({
            'crop': classes,
            'probability': prediction_proba
        }).sort_values('probability', ascending=False)
        
        # Display results
        st.markdown("---")
        st.subheader("🎯 Crop Recommendation Results")
        
        # Main recommendation
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.success(f"**Recommended Crop: {prediction.title()}**")
            st.info(f"**Confidence: {confidence:.1f}%**")
        
        with col2:
            # Crop emoji mapping
            crop_emoji = {
                'rice': '🌾', 'maize': '🌽', 'wheat': '🌾', 'cotton': '🌿',
                'sugarcane': '🌾', 'tomato': '🍅', 'potato': '🥔', 'onion': '🧅',
                'banana': '🍌', 'mango': '🥭', 'grapes': '🍇', 'apple': '🍎',
                'orange': '🍊', 'papaya': '🍈', 'coconut': '🥥', 'coffee': '☕',
                'chickpea': '🫘', 'kidneybeans': '🫘', 'blackgram': '🫘',
                'lentil': '🫘', 'mungbean': '🫘', 'mothbeans': '🫘',
                'pigeonpeas': '🫘', 'jute': '🌿', 'pomegranate': '🍇',
                'watermelon': '🍉', 'muskmelon': '🍈'
            }
            
            emoji = crop_emoji.get(prediction.lower(), '🌱')
            st.markdown(f"<div style='text-align: center; font-size: 4em;'>{emoji}</div>", 
                       unsafe_allow_html=True)
        
        # Top 3 recommendations
        st.subheader("📊 Top 3 Recommendations")
        
        for i, (_, row) in enumerate(proba_df.head(3).iterrows()):
            crop = row['crop']
            prob = row['probability'] * 100
            emoji = crop_emoji.get(crop.lower(), '🌱')
            
            if i == 0:
                st.success(f"{emoji} **{crop.title()}** - {prob:.1f}% confidence")
            elif i == 1:
                st.info(f"{emoji} **{crop.title()}** - {prob:.1f}% confidence")
            else:
                st.warning(f"{emoji} **{crop.title()}** - {prob:.1f}% confidence")
        
        # Feature importance for this prediction
        st.subheader("📈 Key Factors Influencing This Recommendation")
        
        # Get feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Display top 5 features
        st.markdown("**Top 5 Most Important Features:**")
        for i, (_, row) in enumerate(feature_importance.head(5).iterrows()):
            feature = row['feature']
            importance = row['importance'] * 100
            
            # Get the actual value for this feature
            value = input_data[feature]
            
            # Format feature name
            feature_name = feature.replace('_', ' ').title()
            
            st.write(f"{i+1}. **{feature_name}**: {value} (Importance: {importance:.1f}%)")
        
        # Summary statistics
        st.subheader("📋 Input Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Soil Conditions:**")
            st.write(f"- NPK: {N}-{P}-{K}")
            st.write(f"- pH: {ph}")
            st.write(f"- Soil Type: {['Sandy', 'Loamy', 'Clay'][soil_type-1]}")
            st.write(f"- Moisture: {soil_moisture}%")
            st.write(f"- Organic Matter: {organic_matter}%")
        
        with col2:
            st.markdown("**Environmental Conditions:**")
            st.write(f"- Temperature: {temperature}°C")
            st.write(f"- Humidity: {humidity}%")
            st.write(f"- Rainfall: {rainfall} mm")
            st.write(f"- Sunlight: {sunlight_exposure} hours")
            st.write(f"- Wind Speed: {wind_speed} m/s")

# Main interface
def main():
    """Main function to run the enhanced crop interface"""
    show_enhanced_crop_interface()

if __name__ == "__main__":
    main()
