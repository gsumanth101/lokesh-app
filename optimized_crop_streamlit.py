import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

# Load the optimized model
@st.cache_resource
def load_optimized_model():
    """Load the optimized crop recommendation model"""
    try:
        with open('optimized_crop_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        return model_data
    except FileNotFoundError:
        st.error("Optimized model not found. Please run train_optimized_model.py first.")
        return None

def show_optimized_crop_interface():
    """Display the optimized crop recommendation interface"""
    
    st.title("🌾 Optimized Crop Recommendation System")
    st.markdown("""
    ### 🚀 AI-Powered Crop Recommendation with Weather Integration
    This optimized system uses **14 key environmental and soil parameters** to provide highly accurate crop recommendations.
    
    **Model Performance:**
    - **Accuracy:** 99.55%
    - **Crops Supported:** 22 different crops
    - **Features:** 14 optimized parameters
    - **Special Features:** Weather API integration and location-based recommendations
    """)
    
    # Load the model
    model_data = load_optimized_model()
    if model_data is None:
        return
    
    model = model_data['model']
    feature_names = model_data['feature_names']
    soil_type_encoder = model_data['soil_type_encoder']
    water_source_encoder = model_data['water_source_encoder']
    accuracy = model_data['accuracy']
    
    st.success(f"✅ Optimized Model Loaded Successfully! (Accuracy: {accuracy:.2%})")
    
    st.markdown("---")
    
    # Create input interface
    st.subheader("🌱 Enter Crop Parameters")
    
    # Weather data section (will be fetched from NASA Power API)
    st.markdown("**🌤️ Weather Data (API-Integrated)**")
    st.info("💡 In production, these values are automatically fetched from NASA Power API based on your location")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0, step=0.1,
                                     help="Average temperature (fetched from NASA Power API)")
    
    with col2:
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=65.0, step=1.0,
                                  help="Relative humidity (fetched from NASA Power API)")
    
    with col3:
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=3000.0, value=200.0, step=10.0,
                                  help="Annual rainfall (fetched from NASA Power API)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=50.0, value=5.0, step=0.1,
                                    help="Average wind speed (fetched from NASA Power API)")
    
    with col2:
        sunlight_exposure = st.number_input("Sunlight Exposure (hours)", min_value=0.0, max_value=24.0, value=8.0, step=0.1,
                                           help="Daily sunlight exposure (fetched from NASA Power API)")
    
    # User input section
    st.markdown("**🧪 Soil Health Parameters (User Input)**")
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        ph = st.number_input("pH Level", min_value=3.0, max_value=10.0, value=6.5, step=0.1,
                            help="Soil pH level")
    
    with col2:
        organic_matter = st.number_input("Organic Matter (%)", min_value=0.0, max_value=15.0, value=3.0, step=0.1,
                                        help="Organic matter content in soil")
    
    # Location-based parameters
    st.markdown("**📍 Location-Based Parameters (API-Derived)**")
    st.info("💡 In production, these values are automatically derived from your geographical location")
    
    col1, col2 = st.columns(2)
    
    with col1:
        soil_moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0,
                                       help="Current soil moisture (API-derived from location)")
    
    with col2:
        soil_type = st.selectbox("Soil Type", options=[1, 2, 3], 
                                format_func=lambda x: ["Sandy", "Loamy", "Clay"][x-1], index=1,
                                help="Primary soil type (API-derived from location)")
    
    # Environmental and user input
    st.markdown("**🌍 Environmental & User Parameters**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        co2_concentration = st.number_input("CO2 Concentration (ppm)", min_value=300.0, max_value=500.0, value=410.0, step=1.0,
                                           help="Atmospheric CO2 concentration (default/calculated)")
    
    with col2:
        water_source_type = st.selectbox("Water Source Type", options=[1, 2, 3], 
                                        format_func=lambda x: ["Surface Water", "Groundwater", "Rainwater"][x-1], 
                                        index=1, help="Primary water source type (user input)")
    
    # Show feature importance
    st.markdown("---")
    st.subheader("📊 Model Feature Importance")
    
    if 'feature_importance' in model_data:
        importance_df = model_data['feature_importance']
        
        # Create a bar chart
        st.bar_chart(importance_df.set_index('feature')['importance'])
        
        st.markdown("**Top 5 Most Important Features:**")
        for i, (_, row) in enumerate(importance_df.head(5).iterrows()):
            st.write(f"{i+1}. **{row['feature'].replace('_', ' ').title()}**: {row['importance']:.3f}")
    
    # Prediction button
    st.markdown("---")
    if st.button("🌾 Get Crop Recommendation", type="primary"):
        
        # Prepare input data in the exact order expected by the model
        input_data = [
            temperature,           # temperature
            humidity,             # humidity  
            rainfall,             # rainfall
            wind_speed,           # wind_speed
            sunlight_exposure,    # sunlight_exposure
            N,                    # N
            P,                    # P
            K,                    # K
            ph,                   # ph (note: model uses 'ph', not 'pH')
            organic_matter,       # organic_matter
            soil_moisture,        # soil_moisture
            soil_type,            # soil_type (will be encoded)
            co2_concentration,    # co2_concentration
            water_source_type     # water_source_type (will be encoded)
        ]
        
        # Convert to numpy array and reshape
        input_array = np.array(input_data).reshape(1, -1)
        
        try:
            # Make prediction
            prediction = model.predict(input_array)[0]
            prediction_proba = model.predict_proba(input_array)[0]
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
            
            # Input summary
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
                st.write(f"- Water Source: {['Surface Water', 'Groundwater', 'Rainwater'][water_source_type-1]}")
        
        except Exception as e:
            st.error(f"Error making prediction: {e}")
            st.error("Please check that all input values are valid and try again.")

# Main interface
def main():
    """Main function to run the optimized crop interface"""
    st.set_page_config(
        page_title="Optimized Crop Recommendation System",
        page_icon="🌾",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar with model information
    with st.sidebar:
        st.header("🔍 Model Information")
        
        model_data = load_optimized_model()
        if model_data:
            st.success("✅ Model Loaded")
            st.write(f"**Accuracy:** {model_data['accuracy']:.2%}")
            st.write(f"**Features:** {len(model_data['feature_names'])}")
            
            st.subheader("📋 Feature List")
            for i, feature in enumerate(model_data['feature_names'], 1):
                st.write(f"{i}. {feature.replace('_', ' ').title()}")
        
        st.markdown("---")
        st.subheader("🌾 Supported Crops")
        crops = [
            'Apple', 'Banana', 'Blackgram', 'Chickpea', 'Coconut', 
            'Coffee', 'Cotton', 'Grapes', 'Jute', 'Kidneybeans',
            'Lentil', 'Maize', 'Mango', 'Mothbeans', 'Mungbean',
            'Muskmelon', 'Orange', 'Papaya', 'Pigeonpeas', 'Pomegranate',
            'Rice', 'Watermelon'
        ]
        
        for crop in crops:
            st.write(f"🌱 {crop}")
    
    show_optimized_crop_interface()

if __name__ == "__main__":
    main()
