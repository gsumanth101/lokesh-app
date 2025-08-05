#!/usr/bin/env python3
"""
Test script to debug app issues
"""

import sys
import traceback

def test_imports():
    """Test all imports"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        import pandas as pd
        print("✅ Pandas imported successfully")
        
        import numpy as np
        print("✅ Numpy imported successfully")
        
        import requests
        print("✅ Requests imported successfully")
        
        from database import DatabaseManager
        print("✅ DatabaseManager imported successfully")
        
        from googletrans import Translator
        print("✅ Googletrans imported successfully")
        
        # Test database initialization
        db_manager = DatabaseManager()
        print("✅ Database initialized successfully")
        
        # Test translator initialization
        translator = Translator()
        print("✅ Translator initialized successfully")
        
        print("\n🎉 All core imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        print("📋 Full traceback:")
        traceback.print_exc()
        return False

def test_app_functions():
    """Test key app functions"""
    print("\n🧪 Testing app functions...")
    
    try:
        # Import app functions
        from app import get_coordinates_from_location, calculate_advanced_npk
        print("✅ App functions imported successfully")
        
        # Test coordinate function with a simple test
        coords = get_coordinates_from_location("New York")
        if coords:
            print(f"✅ Geocoding test successful: {coords}")
        else:
            print("⚠️ Geocoding test returned None (API might be down)")
        
        # Test NPK calculation with sample data
        sample_soil = {
            'organic_matter': 3.0,
            'pH': 6.5,
            'sand_content': 40,
            'clay_content': 30,
            'silt_content': 30,
            'soil_type': 'Loamy'
        }
        
        enhanced_soil = calculate_advanced_npk(sample_soil)
        print(f"✅ NPK calculation test successful: N={enhanced_soil.get('N')}, P={enhanced_soil.get('P')}, K={enhanced_soil.get('K')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Function test error: {e}")
        print("📋 Full traceback:")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Smart Farming App Diagnostic Test")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test functions
        functions_ok = test_app_functions()
        
        if functions_ok:
            print("\n✅ All tests passed! The app should work correctly.")
            print("🚀 Starting Streamlit app...")
            
            # Try to run streamlit
            import subprocess
            try:
                subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8503"], 
                              check=True)
            except KeyboardInterrupt:
                print("\n🛑 App stopped by user")
            except Exception as e:
                print(f"❌ Error running Streamlit: {e}")
        else:
            print("\n❌ Function tests failed. Please check the error above.")
    else:
        print("\n❌ Import tests failed. Please check the error above.")

if __name__ == "__main__":
    main()
