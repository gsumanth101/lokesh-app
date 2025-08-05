import os
import google.generativeai as genai
import time

# Load API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Choose a Gemini model (using flash model for better quota limits)
model = genai.GenerativeModel("gemini-1.5-flash")

def recommend_crop(soil_type, rainfall_mm, temperature_c, location):
    prompt = f"""
    I am a farmer in {location}.
    Soil type: {soil_type}
    Average rainfall: {rainfall_mm} mm
    Average temperature: {temperature_c} °C
    
    Based on these conditions, suggest the top 3 suitable crops to grow.
    Provide the recommendation in JSON format with fields:
    crop_name, reason, and best_season.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "quota" in str(e).lower() or "rate limit" in str(e).lower():
            print("Rate limit exceeded. Please wait before making another request.")
            print("You can try again in a few minutes or upgrade your API plan.")
        else:
            print(f"An error occurred: {e}")
        return None

# Example usage
print("Getting crop recommendations for Karnataka, India...")
recommendations = recommend_crop("Loamy", 900, 27, "Karnataka, India")
if recommendations:
    print("\nRecommendations:")
    print(recommendations)
else:
    print("\nFailed to get recommendations. Please check your API quota and try again later.")

