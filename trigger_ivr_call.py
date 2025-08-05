# trigger_ivr_call.py

import os
from twilio.rest import Client

# --- Configuration ---
# 1. Your Twilio Account Details (set these as environment variables)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'YOUR_TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'YOUR_TWILIO_AUTH_TOKEN')

# 2. Your Twilio Phone Number
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', 'YOUR_TWILIO_PHONE_NUMBER')

# 3. Your Verified Indian Phone Number
MY_INDIAN_PHONE_NUMBER = "+916303667385"

# 4. The public URL of your running IVR service from ngrok
#    This must point to the NEW entry point of your IVR
IVR_WEBHOOK_URL = "https://72437404f898.ngrok-free.app/ivr/welcome" # <--- UPDATED LINE

# --- Main Script ---
if __name__ == "__main__":
    print(f"📞 Requesting Twilio to call {MY_INDIAN_PHONE_NUMBER}...")

    if "c4fe63b3fae5" in IVR_WEBHOOK_URL or "<your-ngrok-url>" in IVR_WEBHOOK_URL:
        print("❌ ERROR: Please update the 'IVR_WEBHOOK_URL' in this script with your new ngrok URL.")
    else:
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            call = client.calls.create(
                to=MY_INDIAN_PHONE_NUMBER,
                from_=TWILIO_PHONE_NUMBER,
                url=IVR_WEBHOOK_URL
            )

            print(f"✅ Call initiated successfully!")
            print(f"   Call SID: {call.sid}")
            print("   Your phone should be ringing shortly.")

        except Exception as e:
            print(f"❌ Error initiating call: {e}")