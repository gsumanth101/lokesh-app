#!/usr/bin/env python3
"""
Smart Farming SMS Chatbot
Twilio integration for SMS notifications and farmer assistance
"""

from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import logging
from database import DatabaseManager
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'twilio_chatbot_secret_2025'

# Twilio Configuration
TWILIO_ACCOUNT_SID = "AC7c807eb1d55f7800ff8b957ca0dc6953"
TWILIO_AUTH_TOKEN = "477b0363264341452d763829f9b34711"
TWILIO_PHONE_NUMBER = "+15855399486"

# Initialize Twilio client and database
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
db_manager = DatabaseManager()

# Load basic model for SMS recommendations
model = None
try:
    if os.path.exists('crop_recommendation_model.pkl'):
        with open('crop_recommendation_model.pkl', 'rb') as f:
            model = pickle.load(f)
        logger.info("Crop recommendation model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")

# SMS Commands and responses
COMMANDS = {
    'help': 'Available commands:\n• PRICE [crop] - Get market price\n• RECOMMEND - Get crop recommendation\n• WEATHER [location] - Weather info\n• REGISTER - Create account\n• LISTINGS - View crop listings\n• SELL [crop] [qty] [price] - List crop for sale',
    'start': 'Welcome to Smart Farming Assistant! 🌾\nSend HELP for available commands.',
    'hi': 'Hello! Welcome to Smart Farming Assistant. Send HELP for commands.',
    'hello': 'Hello! Welcome to Smart Farming Assistant. Send HELP for commands.'
}

def extract_phone_number(phone):
    """Extract and format phone number"""
    # Remove non-digit characters
    phone = re.sub(r'\D', '', phone)
    
    # Add country code if missing
    if len(phone) == 10:
        phone = '91' + phone
    elif len(phone) == 11 and phone.startswith('0'):
        phone = '91' + phone[1:]
    elif len(phone) == 12 and phone.startswith('91'):
        pass
    else:
        return None
    
    return '+' + phone

def get_market_price(crop_name):
    """Get market price for a crop"""
    try:
        if os.path.exists('data/market_prices.csv'):
            df = pd.read_csv('data/market_prices.csv')
            crop_row = df[df['Crop'].str.lower() == crop_name.lower()]
            if not crop_row.empty:
                price = crop_row.iloc[0]['Price']
                unit = crop_row.iloc[0]['Unit']
                trend = crop_row.iloc[0]['Trend']
                return f"{crop_name.title()}: ₹{price}/{unit}\nTrend: {trend}"
            else:
                return f"Sorry, price for {crop_name} not available."
        else:
            return "Market prices data not available."
    except Exception as e:
        logger.error(f"Error getting market price: {e}")
        return "Error fetching market price."

def get_crop_recommendation_sms(params):
    """Get crop recommendation via SMS with simplified parameters"""
    try:
        if not model:
            return "Crop recommendation service temporarily unavailable."
        
        # Default values for SMS (simplified input)
        features = [
            params.get('N', 80),      # Nitrogen
            params.get('P', 40),      # Phosphorus  
            params.get('K', 40),      # Potassium
            params.get('temp', 25),   # Temperature
            params.get('humidity', 70), # Humidity
            params.get('ph', 6.5),    # pH
            params.get('rainfall', 1000) # Rainfall
        ]
        
        prediction = model.predict([features])[0]
        
        if hasattr(model, 'predict_proba'):
            confidence = model.predict_proba([features]).max() * 100
            return f"Recommended crop: {prediction.title()}\nConfidence: {confidence:.1f}%\n\nFor detailed analysis, use our app!"
        else:
            return f"Recommended crop: {prediction.title()}\n\nFor detailed analysis, use our app!"
            
    except Exception as e:
        logger.error(f"Error in crop recommendation: {e}")
        return "Error generating recommendation."

def get_user_by_phone(phone):
    """Get user information by phone number"""
    try:
        # This is a simplified lookup - in production, you'd have a proper phone-to-user mapping
        # For now, we'll check if phone exists in any user record
        users = db_manager.get_all_users()
        for user in users:
            if user['phone'] and extract_phone_number(user['phone']) == phone:
                return user
        return None
    except Exception as e:
        logger.error(f"Error getting user by phone: {e}")
        return None

@app.route('/sms', methods=['POST'])
def sms_reply():
    """Handle incoming SMS messages"""
    try:
        # Get the message body and sender
        body = request.values.get('Body', '').strip().lower()
        from_number = request.values.get('From', '')
        
        logger.info(f"Received SMS from {from_number}: {body}")
        
        # Create response object
        resp = MessagingResponse()
        msg = resp.message()
        
        # Process the message
        if not body:
            msg.body("Please send a valid command. Send HELP for available commands.")
        elif body in ['help', 'h']:
            msg.body(COMMANDS['help'])
        elif body in ['start', 'hi', 'hello']:
            msg.body(COMMANDS.get(body, COMMANDS['start']))
        elif body.startswith('price '):
            # Extract crop name
            crop_name = body[6:].strip()
            if crop_name:
                price_info = get_market_price(crop_name)
                msg.body(price_info)
            else:
                msg.body("Please specify crop name. Example: PRICE rice")
        elif body == 'recommend':
            # Simple recommendation with default parameters
            recommendation = get_crop_recommendation_sms({})
            msg.body(recommendation)
        elif body.startswith('weather '):
            # Weather command (placeholder - you can integrate with weather API)
            location = body[8:].strip()
            msg.body(f"Weather service for {location} coming soon! Use our app for detailed weather info.")
        elif body == 'register':
            msg.body("To register:\n1. Download our app\n2. Or visit our website\n3. Create account with your phone number\n\nApp link: [Your app link]")
        elif body == 'listings':
            try:
                listings = db_manager.get_crop_listings()[:5]  # Get first 5 listings
                if listings:
                    response_text = "Recent Crop Listings:\n\n"
                    for i, listing in enumerate(listings, 1):
                        response_text += f"{i}. {listing['crop_name'].title()}\n"
                        response_text += f"   {listing['quantity']}kg @ ₹{listing['expected_price']}/kg\n"
                        response_text += f"   Location: {listing.get('location', 'N/A')}\n\n"
                    response_text += "Use our app for complete listings!"
                    msg.body(response_text)
                else:
                    msg.body("No crop listings available at the moment.")
            except Exception as e:
                logger.error(f"Error fetching listings: {e}")
                msg.body("Error fetching listings. Please try again later.")
        elif body.startswith('sell '):
            # Parse sell command: sell [crop] [quantity] [price]
            try:
                parts = body[5:].split()
                if len(parts) >= 3:
                    crop_name = parts[0]
                    quantity = float(parts[1])
                    price = float(parts[2])
                    
                    # Check if user is registered
                    user = get_user_by_phone(from_number)
                    if user and user['role'] in ['farmer', 'agent']:
                        # Create listing (simplified)
                        msg.body(f"Listing request received:\nCrop: {crop_name.title()}\nQty: {quantity}kg\nPrice: ₹{price}/kg\n\nUse our app to complete the listing!")
                    else:
                        msg.body("Please register as a farmer first to create listings. Send REGISTER for instructions.")
                else:
                    msg.body("Invalid format. Use: SELL [crop] [quantity] [price]\nExample: SELL rice 100 45")
            except ValueError:
                msg.body("Invalid numbers in sell command. Use: SELL [crop] [quantity] [price]")
            except Exception as e:
                logger.error(f"Error processing sell command: {e}")
                msg.body("Error processing sell command.")
        else:
            # Try to match partial commands
            if 'price' in body or 'cost' in body:
                msg.body("To check prices, use: PRICE [crop name]\nExample: PRICE rice")
            elif 'crop' in body or 'recommend' in body:
                msg.body("For crop recommendation, send: RECOMMEND")
            elif 'weather' in body:
                msg.body("For weather info, use: WEATHER [location]\nExample: WEATHER Mumbai")
            else:
                msg.body("Command not recognized. Send HELP for available commands.")
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error processing SMS: {e}")
        resp = MessagingResponse()
        resp.message("Sorry, there was an error processing your request. Please try again.")
        return str(resp)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    """Handle incoming WhatsApp messages"""
    try:
        # WhatsApp messages have similar structure to SMS
        body = request.values.get('Body', '').strip().lower()
        from_number = request.values.get('From', '')
        
        logger.info(f"Received WhatsApp from {from_number}: {body}")
        
        # Create response object
        resp = MessagingResponse()
        msg = resp.message()
        
        # Enhanced WhatsApp responses with emojis
        if not body:
            msg.body("Please send a valid command 📱\nSend HELP for available commands.")
        elif body in ['help', 'h']:
            help_text = "🌾 *Smart Farming Assistant*\n\n"
            help_text += "Available commands:\n"
            help_text += "📊 PRICE [crop] - Get market price\n"
            help_text += "🤖 RECOMMEND - Crop recommendation\n"
            help_text += "🌤️ WEATHER [location] - Weather info\n"
            help_text += "📝 REGISTER - Create account\n"
            help_text += "📋 LISTINGS - View crop listings\n"
            help_text += "💰 SELL [crop] [qty] [price] - List crop\n\n"
            help_text += "Example: PRICE rice"
            msg.body(help_text)
        elif body in ['start', 'hi', 'hello']:
            welcome_text = "🌾 Welcome to Smart Farming Assistant!\n\n"
            welcome_text += "Your AI-powered farming companion 🤖\n"
            welcome_text += "Send HELP for available commands"
            msg.body(welcome_text)
        else:
            # Use same logic as SMS but with enhanced formatting for WhatsApp
            return sms_reply()  # Reuse SMS logic
            
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error processing WhatsApp message: {e}")
        resp = MessagingResponse()
        resp.message("❌ Sorry, there was an error. Please try again.")
        return str(resp)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    """API endpoint to send SMS notifications"""
    try:
        data = request.get_json()
        phone_number = data.get('phone')
        message = data.get('message')
        
        if not phone_number or not message:
            return {'success': False, 'error': 'Phone number and message required'}, 400
        
        # Format phone number
        formatted_phone = extract_phone_number(phone_number)
        if not formatted_phone:
            return {'success': False, 'error': 'Invalid phone number'}, 400
        
        # Send SMS
        sms_message = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=formatted_phone
        )
        
        logger.info(f"SMS sent to {formatted_phone}: {sms_message.sid}")
        
        return {
            'success': True,
            'message_id': sms_message.sid,
            'status': sms_message.status
        }
        
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return {'success': False, 'error': str(e)}, 500

@app.route('/broadcast', methods=['POST'])
def broadcast_message():
    """API endpoint to broadcast messages to all farmers"""
    try:
        data = request.get_json()
        message = data.get('message')
        crop_filter = data.get('crop_filter')  # Optional: filter by crop
        
        if not message:
            return {'success': False, 'error': 'Message required'}, 400
        
        # Get farmers to notify
        farmers = db_manager.get_farmers_for_notification(crop_filter)
        sent_count = 0
        
        for farmer in farmers:
            if farmer['phone']:
                try:
                    formatted_phone = extract_phone_number(farmer['phone'])
                    if formatted_phone:
                        twilio_client.messages.create(
                            body=message,
                            from_=TWILIO_PHONE_NUMBER,
                            to=formatted_phone
                        )
                        sent_count += 1
                        logger.info(f"Broadcast sent to {farmer['name']}: {formatted_phone}")
                except Exception as e:
                    logger.error(f"Error sending to {farmer['name']}: {e}")
        
        return {
            'success': True,
            'messages_sent': sent_count,
            'total_farmers': len(farmers)
        }
        
    except Exception as e:
        logger.error(f"Error broadcasting message: {e}")
        return {'success': False, 'error': str(e)}, 500

@app.route('/health')
def health_check():
    """Health check for SMS service"""
    return {
        'status': 'healthy',
        'service': 'SMS Chatbot',
        'timestamp': datetime.now().isoformat(),
        'twilio_connected': bool(twilio_client),
        'model_loaded': model is not None
    }

if __name__ == '__main__':
    print("📱 Starting Smart Farming SMS Chatbot")
    print("=" * 40)
    print(f"🔧 Twilio Account: {TWILIO_ACCOUNT_SID}")
    print(f"📞 Phone Number: {TWILIO_PHONE_NUMBER}")
    print(f"🤖 Model Loaded: {'Yes' if model else 'No'}")
    print(f"🌐 Webhook URL: http://localhost:5000/sms")
    print(f"💬 WhatsApp URL: http://localhost:5000/whatsapp")
    print(f"📡 Broadcast API: http://localhost:5000/broadcast")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
