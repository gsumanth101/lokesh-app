import os
import requests
import json
from datetime import datetime, timedelta
import pandas as pd

class IntelligentCropAdvisor:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    
    def get_nasa_weather_data(self, latitude, longitude):
        """Fetch weather data from NASA Power API"""
        try:
            # NASA Power API endpoint
            base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
            
            # Calculate date range (last 30 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            parameters = [
                'T2M',          # Temperature at 2 Meters
                'PRECTOTCORR',  # Precipitation Corrected
                'RH2M',         # Relative Humidity at 2 Meters
                'WS2M',         # Wind Speed at 2 Meters
                'ALLSKY_SFC_SW_DWN'  # Solar Radiation
            ]
            
            url = f"{base_url}?parameters={','.join(parameters)}&community=AG&longitude={longitude}&latitude={latitude}&start={start_date.strftime('%Y%m%d')}&end={end_date.strftime('%Y%m%d')}&format=JSON"
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return self._process_nasa_data(data)
            else:
                print(f"NASA API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching NASA data: {e}")
            return None
    
    def _process_nasa_data(self, data):
        """Process NASA weather data"""
        try:
            properties = data['properties']['parameter']
            
            # Calculate averages
            avg_temp = sum(properties['T2M'].values()) / len(properties['T2M'])
            avg_precipitation = sum(properties['PRECTOTCORR'].values()) / len(properties['PRECTOTCORR'])
            avg_humidity = sum(properties['RH2M'].values()) / len(properties['RH2M'])
            avg_wind_speed = sum(properties['WS2M'].values()) / len(properties['WS2M'])
            avg_solar_radiation = sum(properties['ALLSKY_SFC_SW_DWN'].values()) / len(properties['ALLSKY_SFC_SW_DWN'])
            
            return {
                'average_temperature': round(avg_temp, 2),
                'average_precipitation': round(avg_precipitation, 2),
                'average_humidity': round(avg_humidity, 2),
                'average_wind_speed': round(avg_wind_speed, 2),
                'average_solar_radiation': round(avg_solar_radiation, 2)
            }
        except Exception as e:
            print(f"Error processing NASA data: {e}")
            return None
    
    def get_crop_recommendations(self, latitude, longitude):
        """Get intelligent crop recommendations using OpenAI"""
        # Get weather data from NASA
        weather_data = self.get_nasa_weather_data(latitude, longitude)
        
        if not weather_data:
            print("Using default location data for recommendations")
            weather_data = {
                'average_temperature': 25,
                'average_precipitation': 5,
                'average_humidity': 65,
                'average_wind_speed': 2,
                'average_solar_radiation': 20
            }
        
        # Current date for seasonal recommendations
        current_date = datetime.now()
        current_month = current_date.strftime("%B")
        current_season = self._get_season(current_date.month)
        
        prompt = f"""
        Based on the following agricultural conditions:
        
        Location: Latitude {latitude}, Longitude {longitude}
        Current Date: {current_date.strftime("%B %d, %Y")}
        Current Season: {current_season}
        
        Weather Data (30-day average):
        - Average Temperature: {weather_data['average_temperature']}°C
        - Average Precipitation: {weather_data['average_precipitation']} mm/day
        - Average Humidity: {weather_data['average_humidity']}%
        - Average Wind Speed: {weather_data['average_wind_speed']} m/s
        - Average Solar Radiation: {weather_data['average_solar_radiation']} MJ/m²/day
        
        Please provide recommendations for 2 different crops that would be suitable for this location and current conditions. For each crop, include:
        
        1. Crop name
        2. Best planting time (specific months)
        3. Expected harvest time
        4. 3 organic pesticides with application details
        5. 3 chemical pesticides with application details
        6. Brief explanation of why this crop is suitable for the current conditions
        
        Format your response as a JSON object with the following structure:
        {{
            "crop_1": {{
                "name": "crop name",
                "planting_time": "best months to plant",
                "harvest_time": "expected harvest months",
                "suitability_reason": "why this crop is suitable",
                "organic_pesticides": [
                    {{
                        "name": "pesticide name",
                        "type": "insecticide/fungicide/herbicide",
                        "application": "how and when to apply",
                        "target": "target pests/diseases"
                    }}
                ],
                "chemical_pesticides": [
                    {{
                        "name": "pesticide name",
                        "type": "insecticide/fungicide/herbicide",
                        "application": "how and when to apply",
                        "target": "target pests/diseases"
                    }}
                ]
            }},
            "crop_2": {{
                "name": "crop name",
                "planting_time": "best months to plant",
                "harvest_time": "expected harvest months",
                "suitability_reason": "why this crop is suitable",
                "organic_pesticides": [
                    {{
                        "name": "pesticide name",
                        "type": "insecticide/fungicide/herbicide",
                        "application": "how and when to apply",
                        "target": "target pests/diseases"
                    }}
                ],
                "chemical_pesticides": [
                    {{
                        "name": "pesticide name",
                        "type": "insecticide/fungicide/herbicide",
                        "application": "how and when to apply",
                        "target": "target pests/diseases"
                    }}
                ]
            }}
        }}
        """
        
        return self._call_openai_api(prompt)
    
    def _get_season(self, month):
        """Determine season based on month (Northern Hemisphere)"""
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"
    
    def _call_openai_api(self, prompt):
        """Make API call to OpenAI"""
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are an expert agricultural advisor with deep knowledge of crop cultivation, pest management, and sustainable farming practices. Always provide practical, location-specific advice."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse as JSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If not valid JSON, return the raw content
                    return {"raw_response": content}
            else:
                print(f"OpenAI API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None
    
    def format_recommendations(self, recommendations):
        """Format the recommendations for display"""
        if not recommendations or "raw_response" in recommendations:
            return recommendations
        
        formatted_output = "\\n🌾 INTELLIGENT CROP RECOMMENDATIONS 🌾\\n"
        formatted_output += "=" * 50 + "\\n\\n"
        
        for i, (crop_key, crop_data) in enumerate(recommendations.items(), 1):
            formatted_output += f"{'🌱' if i == 1 else '🌿'} CROP {i}: {crop_data['name'].upper()}\\n"
            formatted_output += "-" * 30 + "\\n"
            formatted_output += f"📅 Planting Time: {crop_data['planting_time']}\\n"
            formatted_output += f"🌾 Harvest Time: {crop_data['harvest_time']}\\n"
            formatted_output += f"💡 Why This Crop: {crop_data['suitability_reason']}\\n\\n"
            
            # Organic Pesticides
            formatted_output += "🌿 ORGANIC PESTICIDES:\\n"
            for j, pesticide in enumerate(crop_data['organic_pesticides'], 1):
                formatted_output += f"  {j}. {pesticide['name']} ({pesticide['type']})\\n"
                formatted_output += f"     Application: {pesticide['application']}\\n"
                formatted_output += f"     Target: {pesticide['target']}\\n\\n"
            
            # Chemical Pesticides
            formatted_output += "⚗️ CHEMICAL PESTICIDES:\\n"
            for j, pesticide in enumerate(crop_data['chemical_pesticides'], 1):
                formatted_output += f"  {j}. {pesticide['name']} ({pesticide['type']})\\n"
                formatted_output += f"     Application: {pesticide['application']}\\n"
                formatted_output += f"     Target: {pesticide['target']}\\n\\n"
            
            formatted_output += "\\n" + "=" * 50 + "\\n\\n"
        
        return formatted_output

def main():
    """Main function to demonstrate the crop advisor"""
    try:
        advisor = IntelligentCropAdvisor()
        
        # Example coordinates (Bangalore, India)
        latitude = 12.9716
        longitude = 77.5946
        
        print("🌾 Getting intelligent crop recommendations...")
        print(f"📍 Location: {latitude}, {longitude}")
        print("🌡️ Fetching weather data from NASA Power API...")
        
        recommendations = advisor.get_crop_recommendations(latitude, longitude)
        
        if recommendations:
            formatted_output = advisor.format_recommendations(recommendations)
            print(formatted_output)
            
            # Save recommendations to file
            with open(f'crop_recommendations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
                json.dump(recommendations, f, indent=2)
            print("📁 Recommendations saved to file!")
            
        else:
            print("❌ Failed to get recommendations. Please check your API key and connection.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
