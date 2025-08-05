#!/usr/bin/env python3
"""
Complete application startup script
Runs both Streamlit frontend and Flask chatbot backend
"""

import subprocess
import threading
import time
import os
import sys

def run_streamlit():
    """Run the Streamlit application"""
    print("🌾 Starting Streamlit Frontend...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], 
                      check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Streamlit stopped by user")

def run_flask_chatbot():
    """Run the Flask chatbot application"""
    print("🤖 Starting Flask Chatbot Backend...")
    try:
        subprocess.run([sys.executable, "twilio_chatbot.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Flask chatbot: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Flask chatbot stopped by user")

def main():
    """Main function to start both applications"""
    print("🚀 Smart Farming Assistant - Complete Application")
    print("=" * 60)
    print("Starting both Streamlit frontend and Flask chatbot backend...")
    print()
    
    # Start Flask chatbot in a separate thread
    flask_thread = threading.Thread(target=run_flask_chatbot, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(3)
    
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()
    
    print("\n🌟 Applications are starting up...")
    print("📱 Streamlit Frontend: http://localhost:8501")
    print("🤖 Flask Chatbot Backend: http://localhost:5000")
    print("📱 SMS Webhook: http://localhost:5000/sms")
    print("💬 WhatsApp Webhook: http://localhost:5000/whatsapp")
    print("\n✋ Press Ctrl+C to stop both applications")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down applications...")
        print("✅ Applications stopped successfully!")

if __name__ == "__main__":
    main()
