# Smart Farming Assistant

A Streamlit-based web application that helps farmers increase their income and avoid losses by providing crop recommendations based on real-time weather data and soil conditions. This app aligns with SDG Goal 2: Zero Hunger.

## Features

- **Real-time Weather Data**: Fetches current weather conditions using OpenWeatherMap API
- **Soil Condition Analysis**: Analyzes soil nutrients (N, P, K), pH, and rainfall data
- **Machine Learning Crop Recommendation**: Uses trained Decision Tree/Random Forest models
- **Pesticide Recommendations**: Provides appropriate pesticide type and application details
- **Market Price Information**: Shows current market prices and trends
- **Multilingual Support**: Supports English, Hindi, and Telugu languages
- **User-friendly Interface**: Clean and intuitive Streamlit interface

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   # If you have git installed
   git clone <repository-url>
   
   # Or download and extract the project files
   ```

2. **Navigate to Project Directory**
   ```bash
   cd smart-farming-assistant
   ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get WeatherAPI Key**
   - Visit [WeatherAPI](https://www.weatherapi.com/)
   - Sign up for a free account
   - Generate your API key

5. **Train the Machine Learning Model**
   ```bash
   python train_model.py
   ```

6. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Start the Application**
   - Open your terminal/command prompt
   - Navigate to the project directory
   - Run: `streamlit run app.py`
   - The app will open in your default web browser

2. **Configure the App**
   - Enter your WeatherAPI key in the sidebar
   - Select your preferred language (English/Hindi/Telugu)

3. **Get Crop Recommendations**
   - Enter your city or district name
   - The app will automatically:
     - Fetch current weather data
     - Analyze soil conditions
     - Recommend the best crop
     - Show pesticide recommendations
     - Display market prices

## File Structure

```
smart-farming-assistant/
├── app.py                 # Main Streamlit application
├── model.py              # Simple model training script
├── train_model.py        # Enhanced model training with comprehensive data
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── data/
│   ├── soil_data.csv           # Sample soil data
│   ├── market_prices.csv       # Market price data
│   ├── pesticides.csv          # Pesticide recommendations
│   └── comprehensive_crop_data.csv # Generated training data
└── crop_recommendation_model.pkl  # Trained ML model (generated)
```

## Data Sources

### Weather Data
- **Source**: WeatherAPI
- **Data**: Temperature, humidity, weather conditions
- **Update Frequency**: Real-time

### Soil Data
- **Current**: Dummy CSV data (for demonstration)
- **Future**: Can be integrated with SoilGrids API
- **Parameters**: N, P, K, pH, rainfall

### Market Prices
- **Source**: Static CSV data (sample)
- **Data**: Current prices, trends, last updated dates
- **Note**: In production, this would connect to live market data APIs

### Pesticide Information
- **Source**: Static CSV database
- **Data**: Pesticide type, application amount, timing

## Machine Learning Model

### Algorithm
- **Primary**: Random Forest Classifier
- **Fallback**: Decision Tree Classifier
- **Selection**: Automatically selects best performing model

### Features
- Temperature (°C)
- Humidity (%)
- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- pH Level
- Rainfall (mm)

### Supported Crops
- Wheat
- Rice
- Maize
- Cotton
- Sugarcane
- Tomato
- Potato
- Onion
- Barley
- Millet

## Customization

### Adding New Crops
1. Update `train_model.py` to include new crop data
2. Add market price data to `data/market_prices.csv`
3. Add pesticide information to `data/pesticides.csv`
4. Retrain the model: `python train_model.py`

### Updating Market Prices
- Edit `data/market_prices.csv` with current prices
- The app will automatically use updated data

### Adding New Languages
- Modify the `language_options` dictionary in `app.py`
- Add language codes supported by Google Translate

## API Integration

### WeatherAPI
- **Endpoint**: `http://api.weatherapi.com/v1/current.json`
- **Parameters**: Location, API key, air quality data
- **Rate Limit**: 1000 calls/day (free tier)

### Future Integrations
- **SoilGrids API**: For real soil data
- **Market Data APIs**: For live price information
- **Satellite Data**: For advanced crop monitoring

## Troubleshooting

### Common Issues

1. **Module Not Found Error**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   - Verify your WeatherAPI key is correct
   - Check if the API key is active (may take a few minutes after creation)

3. **Model File Missing**
   ```bash
   python train_model.py
   ```

4. **Translation Errors**
   - Check internet connection
   - Google Translate API may have rate limits

### Performance Tips

- **Large Cities**: Use specific city names for better accuracy
- **Rural Areas**: Try using district or state names
- **Slow Loading**: API calls may take time depending on connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue in the repository

## Acknowledgments

- WeatherAPI for weather data API
- Scikit-learn for machine learning capabilities
- Streamlit for the web framework
- Google Translate for multilingual support

---

**Note**: This is a demonstration application. For production use, consider implementing proper error handling, data validation, and security measures.
