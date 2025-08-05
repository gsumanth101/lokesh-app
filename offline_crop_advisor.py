import json
from datetime import datetime
import requests

class OfflineCropAdvisor:
    def __init__(self):
        self.crop_database = {
            "rice": {
                "name": "Rice",
                "planting_time": "June-July (Kharif) or December-January (Rabi)",
                "harvest_time": "November-December (Kharif) or April-May (Rabi)",
                "suitability_reason": "Rice thrives in warm, humid conditions with abundant water supply. Ideal for areas with average temperature 20-35°C and high rainfall or irrigation.",
                "organic_pesticides": [
                    {
                        "name": "Neem Oil",
                        "type": "Insecticide/Fungicide",
                        "application": "Spray 3-5ml per liter of water every 10-15 days",
                        "target": "Brown planthopper, stem borer, blast disease"
                    },
                    {
                        "name": "Bacillus thuringiensis (Bt)",
                        "type": "Biological Insecticide",
                        "application": "Apply 1-2 kg per hectare during early larval stage",
                        "target": "Yellow stem borer, leaf folder"
                    },
                    {
                        "name": "Trichoderma",
                        "type": "Biological Fungicide",
                        "application": "Seed treatment 4-10g per kg of seed or soil application",
                        "target": "Sheath blight, root rot"
                    }
                ],
                "chemical_pesticides": [
                    {
                        "name": "Carbofuran 3G",
                        "type": "Systemic Insecticide",
                        "application": "Apply 33 kg per hectare at transplanting",
                        "target": "Stem borer, brown planthopper, whorl maggot"
                    },
                    {
                        "name": "Tricyclazole 75% WP",
                        "type": "Systemic Fungicide",
                        "application": "Spray 0.6g per liter at boot leaf stage",
                        "target": "Blast disease"
                    },
                    {
                        "name": "Pretilachlor 50% EC",
                        "type": "Pre-emergence Herbicide",
                        "application": "Apply 1-1.5 liter per hectare 3-5 days after transplanting",
                        "target": "Annual grasses and broad-leaf weeds"
                    }
                ]
            },
            "maize": {
                "name": "Maize (Corn)",
                "planting_time": "June-July (Kharif) or November-December (Rabi)",
                "harvest_time": "September-October (Kharif) or March-April (Rabi)",
                "suitability_reason": "Maize is adaptable to various climates and requires moderate rainfall. Grows well in temperature range of 15-35°C with well-drained soils.",
                "organic_pesticides": [
                    {
                        "name": "Neem Seed Kernel Extract (NSKE)",
                        "type": "Insecticide",
                        "application": "Spray 5% solution every 15 days",
                        "target": "Fall armyworm, stem borer, aphids"
                    },
                    {
                        "name": "Beauveria bassiana",
                        "type": "Entomopathogenic Fungus",
                        "application": "Apply 5-10g per liter of water",
                        "target": "White grub, termites, thrips"
                    },
                    {
                        "name": "Pheromone Traps",
                        "type": "Biological Control",
                        "application": "Install 5-8 traps per hectare",
                        "target": "Fall armyworm, stem borer moths"
                    }
                ],
                "chemical_pesticides": [
                    {
                        "name": "Chlorantraniliprole 18.5% SC",
                        "type": "Insecticide",
                        "application": "Spray 150ml per hectare",
                        "target": "Fall armyworm, stem borer"
                    },
                    {
                        "name": "Propiconazole 25% EC",
                        "type": "Systemic Fungicide",
                        "application": "Spray 1ml per liter of water",
                        "target": "Turcicum leaf blight, rust"
                    },
                    {
                        "name": "Atrazine 50% WP",
                        "type": "Pre-emergence Herbicide",
                        "application": "Apply 1-2 kg per hectare within 3 days of sowing",
                        "target": "Annual grasses and broad-leaf weeds"
                    }
                ]
            },
            "tomato": {
                "name": "Tomato",
                "planting_time": "July-August (Kharif) or December-January (Rabi)",
                "harvest_time": "October-November (Kharif) or March-May (Rabi)",
                "suitability_reason": "Tomatoes prefer moderate temperatures (18-29°C) and well-drained soils. Suitable for areas with controlled water supply and good sunlight.",
                "organic_pesticides": [
                    {
                        "name": "Bacillus subtilis",
                        "type": "Biological Fungicide",
                        "application": "Spray 2-3g per liter of water every 10 days",
                        "target": "Early blight, late blight, bacterial wilt"
                    },
                    {
                        "name": "Chrysoperla carnea",
                        "type": "Predatory Insect",
                        "application": "Release 5000-10000 eggs per hectare",
                        "target": "Aphids, whiteflies, thrips"
                    },
                    {
                        "name": "Garlic-Chili Extract",
                        "type": "Natural Repellent",
                        "application": "Spray 10ml per liter every week",
                        "target": "Aphids, spider mites, minor insects"
                    }
                ],
                "chemical_pesticides": [
                    {
                        "name": "Imidacloprid 17.8% SL",
                        "type": "Systemic Insecticide",
                        "application": "Spray 0.3ml per liter of water",
                        "target": "Whiteflies, aphids, thrips"
                    },
                    {
                        "name": "Mancozeb 75% WP",
                        "type": "Contact Fungicide",
                        "application": "Spray 2g per liter of water every 10-15 days",
                        "target": "Early blight, late blight"
                    },
                    {
                        "name": "Pendimethalin 30% EC",
                        "type": "Pre-emergence Herbicide",
                        "application": "Apply 3.3ml per liter within 3 days of transplanting",
                        "target": "Annual grasses and broad-leaf weeds"
                    }
                ]
            },
            "wheat": {
                "name": "Wheat",
                "planting_time": "November-December (Rabi season)",
                "harvest_time": "April-May",
                "suitability_reason": "Wheat is a cool-season crop that requires moderate temperatures (15-25°C) and well-distributed rainfall. Ideal for winter cultivation in temperate regions.",
                "organic_pesticides": [
                    {
                        "name": "Neem Cake",
                        "type": "Soil Amendment/Insecticide",
                        "application": "Apply 200-250 kg per hectare during land preparation",
                        "target": "Termites, root grubs, soil-borne diseases"
                    },
                    {
                        "name": "Trichogramma",
                        "type": "Parasitic Wasp",
                        "application": "Release 50000 adults per hectare at 15-day intervals",
                        "target": "Armyworm, stem borer"
                    },
                    {
                        "name": "Copper Sulfate (Bordeaux mixture)",
                        "type": "Organic Fungicide",
                        "application": "Spray 1% solution every 15 days",
                        "target": "Rust diseases, smut"
                    }
                ],
                "chemical_pesticides": [
                    {
                        "name": "Propiconazole 25% EC",
                        "type": "Systemic Fungicide",
                        "application": "Spray 0.1% solution at boot leaf stage",
                        "target": "Yellow rust, brown rust, powdery mildew"
                    },
                    {
                        "name": "Quinalphos 25% EC",
                        "type": "Contact Insecticide",
                        "application": "Spray 2ml per liter of water",
                        "target": "Aphids, termites, armyworm"
                    },
                    {
                        "name": "2,4-D Ethyl Ester 38% EC",
                        "type": "Selective Herbicide",
                        "application": "Spray 2ml per liter 30-35 days after sowing",
                        "target": "Broad-leaf weeds"
                    }
                ]
            },
            "cotton": {
                "name": "Cotton",
                "planting_time": "April-May (Kharif season)",
                "harvest_time": "October-January (multiple pickings)",
                "suitability_reason": "Cotton requires warm temperatures (21-30°C) and moderate to high rainfall. Suitable for areas with long growing season and adequate irrigation facilities.",
                "organic_pesticides": [
                    {
                        "name": "Nuclear Polyhedrosis Virus (NPV)",
                        "type": "Biological Insecticide",
                        "application": "Apply 250-500 LE per hectare in evening",
                        "target": "Bollworm complex (American, pink, spotted)"
                    },
                    {
                        "name": "Verticillium lecanii",
                        "type": "Entomopathogenic Fungus",
                        "application": "Spray 5g per liter of water",
                        "target": "Whiteflies, aphids, thrips"
                    },
                    {
                        "name": "Castor Oil",
                        "type": "Natural Insecticide",
                        "application": "Spray 10ml per liter with surfactant",
                        "target": "Sucking pests, leaf-eating caterpillars"
                    }
                ],
                "chemical_pesticides": [
                    {
                        "name": "Emamectin Benzoate 5% SG",
                        "type": "Insecticide",
                        "application": "Spray 4g per 10 liters of water",
                        "target": "American bollworm, pink bollworm"
                    },
                    {
                        "name": "Thiamethoxam 25% WG",
                        "type": "Systemic Insecticide",
                        "application": "Spray 0.2g per liter of water",
                        "target": "Whiteflies, aphids, jassids"
                    },
                    {
                        "name": "Pendimethalin 30% EC",
                        "type": "Pre-emergence Herbicide",
                        "application": "Apply 1 liter per hectare within 3 days of sowing",
                        "target": "Annual grasses and broad-leaf weeds"
                    }
                ]
            },
            "sugarcane": {
                "name": "Sugarcane",
                "planting_time": "February-April (Spring) or October-November (Autumn)",
                "harvest_time": "12-18 months after planting",
                "suitability_reason": "Sugarcane requires warm temperatures (26-32°C) and high water availability. Suitable for tropical and subtropical regions with long growing seasons.",
                "organic_pesticides": [
                    {
                        "name": "Metarhizium anisopliae",
                        "type": "Entomopathogenic Fungus",
                        "application": "Apply 5-10g per liter of water to soil",
                        "target": "White grub, root borer, termites"
                    },
                    {
                        "name": "Pseudomonas fluorescens",
                        "type": "Bacterial Biocontrol",
                        "application": "Sett treatment 10g per liter before planting",
                        "target": "Red rot, wilt diseases"
                    },
                    {
                        "name": "Pongamia Oil",
                        "type": "Botanical Insecticide",
                        "application": "Spray 10ml per liter with sticker",
                        "target": "Scale insects, mealybugs, aphids"
                    }
                ],
                "chemical_pesticides": [
                    {
                        "name": "Chlorpyrifos 20% EC",
                        "type": "Contact Insecticide",
                        "application": "Apply 2.5 liters per hectare to soil",
                        "target": "Termites, white grub, root borer"
                    },
                    {
                        "name": "Carbendazim 50% WP",
                        "type": "Systemic Fungicide",
                        "application": "Sett treatment 2g per liter of water",
                        "target": "Red rot, smut, wilt diseases"
                    },
                    {
                        "name": "Atrazine 50% WP",
                        "type": "Pre-emergence Herbicide",
                        "application": "Apply 2 kg per hectare after planting",
                        "target": "Annual and perennial weeds"
                    }
                ]
            }
        }
    
    def get_nasa_weather_data(self, latitude, longitude):
        """Fetch weather data from NASA Power API"""
        try:
            # NASA Power API endpoint
            base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
            
            # Calculate date range (last 30 days)
            from datetime import datetime, timedelta
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
            
            response = requests.get(url, timeout=10)
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
        """Get crop recommendations based on location and season"""
        # Get weather data from NASA
        weather_data = self.get_nasa_weather_data(latitude, longitude)
        
        if not weather_data:
            print("Using default weather data for recommendations")
            weather_data = {
                'average_temperature': 25,
                'average_precipitation': 5,
                'average_humidity': 65,
                'average_wind_speed': 2,
                'average_solar_radiation': 20
            }
        
        # Current date for seasonal recommendations
        current_date = datetime.now()
        current_month = current_date.month
        current_season = self._get_season(current_month)
        
        print(f"📊 Weather Data (30-day average from NASA Power API):")
        print(f"   🌡️  Temperature: {weather_data['average_temperature']}°C")
        print(f"   🌧️  Precipitation: {weather_data['average_precipitation']} mm/day")
        print(f"   💧 Humidity: {weather_data['average_humidity']}%")
        print(f"   💨 Wind Speed: {weather_data['average_wind_speed']} m/s")
        print(f"   ☀️  Solar Radiation: {weather_data['average_solar_radiation']} MJ/m²/day")
        print(f"   📅 Current Season: {current_season}")
        print()
        
        # Select appropriate crops based on season and weather
        recommended_crops = self._select_crops_by_season_and_weather(
            current_month, weather_data['average_temperature']
        )
        
        return {
            "weather_data": weather_data,
            "recommendations": {
                "crop_1": self.crop_database[recommended_crops[0]],
                "crop_2": self.crop_database[recommended_crops[1]]
            }
        }
    
    def _get_season(self, month):
        """Determine season based on month (Indian agricultural seasons)"""
        if month in [6, 7, 8, 9]:  # Monsoon/Kharif
            return "Kharif (Monsoon)"
        elif month in [10, 11, 12, 1, 2, 3]:  # Winter/Rabi
            return "Rabi (Winter)"
        else:  # Summer
            return "Zaid (Summer)"
    
    def _select_crops_by_season_and_weather(self, month, temperature):
        """Select crops based on current season and temperature"""
        if month in [6, 7, 8, 9]:  # Kharif season
            if temperature > 25:
                return ["rice", "cotton"]
            else:
                return ["maize", "rice"]
        elif month in [10, 11, 12, 1, 2]:  # Rabi season
            return ["wheat", "tomato"]
        elif month in [3, 4, 5]:  # Summer/Zaid season
            if temperature > 30:
                return ["sugarcane", "cotton"]
            else:
                return ["maize", "tomato"]
        else:
            return ["rice", "maize"]  # Default
    
    def format_recommendations(self, result):
        """Format the recommendations for display"""
        recommendations = result["recommendations"]
        weather_data = result["weather_data"]
        
        formatted_output = "\n🌾 INTELLIGENT CROP RECOMMENDATIONS 🌾\n"
        formatted_output += "=" * 60 + "\n\n"
        
        for i, (crop_key, crop_data) in enumerate(recommendations.items(), 1):
            formatted_output += f"{'🌱' if i == 1 else '🌿'} CROP {i}: {crop_data['name'].upper()}\n"
            formatted_output += "-" * 40 + "\n"
            formatted_output += f"📅 Planting Time: {crop_data['planting_time']}\n"
            formatted_output += f"🌾 Harvest Time: {crop_data['harvest_time']}\n"
            formatted_output += f"💡 Why This Crop: {crop_data['suitability_reason']}\n\n"
            
            # Organic Pesticides
            formatted_output += "🌿 ORGANIC PESTICIDES:\n"
            for j, pesticide in enumerate(crop_data['organic_pesticides'], 1):
                formatted_output += f"  {j}. {pesticide['name']} ({pesticide['type']})\n"
                formatted_output += f"     Application: {pesticide['application']}\n"
                formatted_output += f"     Target: {pesticide['target']}\n\n"
            
            # Chemical Pesticides
            formatted_output += "⚗️ CHEMICAL PESTICIDES:\n"
            for j, pesticide in enumerate(crop_data['chemical_pesticides'], 1):
                formatted_output += f"  {j}. {pesticide['name']} ({pesticide['type']})\n"
                formatted_output += f"     Application: {pesticide['application']}\n"
                formatted_output += f"     Target: {pesticide['target']}\n\n"
            
            formatted_output += "=" * 60 + "\n\n"
        
        return formatted_output

def main():
    """Main function to demonstrate the offline crop advisor"""
    try:
        advisor = OfflineCropAdvisor()
        
        # Example coordinates (Bangalore, India)
        latitude = 12.9716
        longitude = 77.5946
        
        print("🌾 Getting intelligent crop recommendations...")
        print(f"📍 Location: {latitude}, {longitude}")
        print("🌡️ Fetching weather data from NASA Power API...\n")
        
        result = advisor.get_crop_recommendations(latitude, longitude)
        
        if result:
            formatted_output = advisor.format_recommendations(result)
            print(formatted_output)
            
            # Save recommendations to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f'crop_recommendations_{timestamp}.json', 'w') as f:
                json.dump(result, f, indent=2)
            print(f"📁 Recommendations saved to crop_recommendations_{timestamp}.json!")
            
        else:
            print("❌ Failed to get recommendations.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
