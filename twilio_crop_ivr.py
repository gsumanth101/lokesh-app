# twilio_crop_ivr.py

import os
import requests
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# --- Configuration ---
WEB_APP_API_URL = "http://127.0.0.1:5000/api/crop-recommendation"
# In twilio_crop_ivr.py (at the top)
DISEASE_API_URL = "http://127.0.0.1:5000/api/predict-disease"
AGENT_PHONE_NUMBER = "+919876543210"  # IMPORTANT: Replace with the real agent's phone number

# --- Helper Functions ---

def get_recommendation_from_api(location: str) -> str:
    """Sends a request to your web_app.py backend to get a crop recommendation."""
    try:
        print(f"IVR: Sending API request for location '{location}'...")
        payload = {"location": location, "model_type": "basic"}
        response = requests.post(WEB_APP_API_URL, json=payload, timeout=25)
        
        if response.status_code == 200:
            data = response.json()
            return data['data']['recommended_crop'].capitalize() if data.get('success') else data.get('message', "Could not get a recommendation.")
        else:
            return "Sorry, the recommendation service is not responding correctly."
    except Exception as e:
        print(f"ERROR: Could not connect to the web_app.py server: {e}")
        return "Sorry, the recommendation service is currently unavailable."

def get_disease_from_api(crop_name: str) -> str:
    """Calls the web_app.py backend to get a disease prediction."""
    try:
        print(f"IVR: Sending disease prediction request for '{crop_name}'...")
        payload = {"crop_name": crop_name}
        response = requests.post(DISEASE_API_URL, json=payload, timeout=25)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                prediction_data = data['data']
                if prediction_data['status'] == 'healthy':
                    return "Conditions are favorable for a healthy crop. No major diseases detected."
                else:
                    disease = prediction_data.get('primary_disease', 'a potential disease')
                    risk = prediction_data.get('overall_risk', 'moderate')
                    return f"There is a {risk} risk for {disease}. Please check the app for detailed prevention tips."
            else:
                return data.get('message', "Could not get disease information.")
        else:
            return "Sorry, the disease prediction service is not responding correctly."

    except Exception as e:
        print(f"ERROR: Could not connect to disease API: {e}")
        return "Sorry, the disease prediction service is currently unavailable."

@app.route("/ivr/welcome", methods=['POST'])
def welcome():
    """Step 1: Welcome the caller and ask for language preference."""
    response = VoiceResponse()
    
    # Use the explicit method to build the TwiML
    gather = Gather(num_digits=1, action='/ivr/menu', method='POST')
    gather.say("Welcome to the Smart Farming Assistant.", language='en-IN')
    gather.say("हिंदी के लिए 2 दबाएं.", language='hi-IN')
    response.append(gather)
    
    # Fallback if user enters nothing
    response.redirect('/ivr/welcome')
    return str(response)

@app.route("/ivr/menu", methods=['POST'])
def menu():
    """Step 2: Present the main menu in the chosen language."""
    selected_lang = request.values.get('Digits')
    response = VoiceResponse()
    action_url = f'/ivr/action-handler?lang={selected_lang}'
    
    gather = Gather(num_digits=1, action=action_url, method='POST')
    if selected_lang == '2': # Hindi
        gather.say("फसल की सिफारिश के लिए 1 दबाएं.", language='hi-IN')
        gather.say("एजेंट से बात करने के लिए 2 दबाएं.", language='hi-IN')
        gather.say("फसल रोग की जानकारी के लिए 3 दबाएं.", language='hi-IN')
    else: # Default to English
        gather.say("For crop recommendation, press 1.", language='en-IN')
        gather.say("To speak with an agent, press 2.", language='en-IN')
        gather.say("For crop disease information, press 3.", language='en-IN')
    response.append(gather)

    response.redirect(f'/ivr/menu?Digits={selected_lang}')
    return str(response)

@app.route("/ivr/action-handler", methods=['POST'])
def action_handler():
    """Step 3: Handle the user's choice from the main menu."""
    choice = request.values.get('Digits')
    lang = request.args.get('lang', '1')
    response = VoiceResponse()
    
    is_hindi = (lang == '2')
    lang_code = 'hi-IN' if is_hindi else 'en-IN'

    if choice == '1': # Crop Recommendation
        action_url = f'/ivr/handle-recommendation?lang={lang}'
        prompt = "कृपया अपने शहर का नाम बताएं।" if is_hindi else "Please say the name of your city."
        gather = Gather(input='speech', speechTimeout=4, language=lang_code, action=action_url, method='POST')
        gather.say(prompt, language=lang_code)
        response.append(gather)
        response.redirect(f'/ivr/action-handler?lang={lang}&Digits=1')

    elif choice == '2': # Call Agent
        prompt = "आपको अब हमारे एजेंट से जोड़ा जा रहा है।" if is_hindi else "Connecting you to an agent now."
        response.say(prompt, language=lang_code)
        response.dial(AGENT_PHONE_NUMBER)
        
    elif choice == '3': # Disease Prediction
        action_url = f'/ivr/handle-disease?lang={lang}'
        prompt = "कृपया फसल का नाम बताएं।" if is_hindi else "Please say the name of the crop."
        gather = Gather(input='speech', speechTimeout=4, language=lang_code, action=action_url, method='POST')
        gather.say(prompt, language=lang_code)
        response.append(gather)
        response.redirect(f'/ivr/action-handler?lang={lang}&Digits=3')
            
    else:
        prompt = "अमान्य विकल्प। कृपया दोबारा फोन करें।" if is_hindi else "Invalid choice. Please call again."
        response.say(prompt, language=lang_code)
        response.hangup()
        
    return str(response)

@app.route("/ivr/handle-recommendation", methods=['POST'])
def handle_recommendation():
    """Step 4a: Process location, get recommendation, and provide output."""
    location = request.values.get("SpeechResult", "").strip()
    lang = request.args.get('lang', '1')
    is_hindi = (lang == '2')
    lang_code = 'hi-IN' if is_hindi else 'en-IN'
    response = VoiceResponse()

    if not location:
        prompt = "माफ़ कीजिए, मैं आपका स्थान नहीं सुन सका।" if is_hindi else "Sorry, I could not hear your location."
        response.say(prompt, language=lang_code)
    else:
        wait_prompt = f"{location} के लिए सिफारिश प्राप्त की जा रही है। कृपया प्रतीक्षा करें।" if is_hindi else f"Getting recommendation for {location}. Please wait."
        response.say(wait_prompt, language=lang_code)
        
        recommended_crop = get_recommendation_from_api(location)
        
        message = f"{location} के लिए, अनुशंसित फसल है {recommended_crop}।" if is_hindi else f"For {location}, the recommended crop is {recommended_crop}."
        response.say(message, language=lang_code, voice='Polly.Aditi')

    goodbye_prompt = "कॉल करने के लिए धन्यवाद। अलविदा।" if is_hindi else "Thank you for calling. Goodbye."
    response.say(goodbye_prompt, language=lang_code)
    response.hangup()
    return str(response)

@app.route("/ivr/handle-disease", methods=['POST'])
def handle_disease():
    """Processes crop name, calls the disease API, and provides voice output."""
    crop_name = request.values.get("SpeechResult", "").strip()
    lang = request.args.get('lang', '1')
    is_hindi = (lang == '2')
    lang_code = 'hi-IN' if is_hindi else 'en-IN'
    response = VoiceResponse()

    if not crop_name:
        prompt = "माफ़ कीजिए, मैं फसल का नाम नहीं सुन सका।" if is_hindi else "Sorry, I could not hear the crop name."
        response.say(prompt, language=lang_code)
    else:
        wait_prompt = f"{crop_name} के लिए रोग की जानकारी प्राप्त की जा रही है।" if is_hindi else f"Getting disease information for {crop_name}."
        response.say(wait_prompt, language=lang_code)

        disease_info = get_disease_from_api(crop_name)
        
        response.say(disease_info, language='en-IN', voice='Polly.Aditi')
        
    goodbye_prompt = "कॉल करने के लिए धन्यवाद। अलविदा।" if is_hindi else "Thank you for calling. Goodbye."
    response.say(goodbye_prompt, language=lang_code)
    response.hangup()
    return str(response)
if __name__ == '__main__':
    # Run on a different port than your other services
    app.run(port=5003, debug=True, use_reloader=False)
