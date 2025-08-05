#!/usr/bin/env python3
"""
Test script for weekend farming distance calculation functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from app import calculate_distance, get_location_coordinates

def test_distance_calculation():
    """Test the distance calculation functionality"""
    print("=== Testing Distance Calculation Functionality ===")
    
    # Test locations
    test_locations = [
        ("Bangalore, Karnataka, India", "Mysore, Karnataka, India"),
        ("Mumbai, Maharashtra, India", "Pune, Maharashtra, India"),
        ("Delhi, India", "Gurgaon, Haryana, India")
    ]
    
    google_maps_api_key = 'AIzaSyD8HeI8o-c1NXmY7EZ_W7HhbpqOgO_xTLo'
    
    for origin, destination in test_locations:
        print(f"\n🗺️ Testing route: {origin} -> {destination}")
        
        # Test coordinate retrieval
        origin_coords = get_location_coordinates(origin)
        dest_coords = get_location_coordinates(destination)
        
        print(f"📍 Origin coordinates: {origin_coords}")
        print(f"📍 Destination coordinates: {dest_coords}")
        
        # Test distance calculation
        distance_result = calculate_distance(origin, destination, google_maps_api_key)
        
        if distance_result['success']:
            print(f"✅ Distance calculation successful!")
            print(f"   Distance: {distance_result['distance_text']}")
            print(f"   Duration: {distance_result['duration_text']}")
            print(f"   Method: {distance_result['method']}")
        else:
            print(f"❌ Distance calculation failed: {distance_result.get('error', 'Unknown error')}")

def test_database_operations():
    """Test database operations for weekend farming"""
    print("\n=== Testing Database Operations ===")
    
    db_manager = DatabaseManager()
    
    # Test user location retrieval
    print("\n🔍 Testing user location retrieval...")
    
    # Test with a sample user ID (you may need to adjust this)
    test_user_id = 1
    user_location = db_manager.get_user_location(test_user_id)
    print(f"User {test_user_id} location: {user_location}")
    
    # Test getting farming availability
    print("\n🏡 Testing farm availability retrieval...")
    farms = db_manager.get_farming_availability()
    print(f"Found {len(farms)} farms:")
    
    for farm in farms[:3]:  # Show first 3 farms
        print(f"  - {farm['farmer_name']} at {farm['location']} ({farm['available_acres']} acres)")

def test_weekend_farmer_authentication():
    """Test weekend farmer authentication"""
    print("\n=== Testing Weekend Farmer Authentication ===")
    
    db_manager = DatabaseManager()
    
    # Test weekend farmer credentials
    weekend_farmer_email = "weekendfarmer@smartfarm.com"
    weekend_farmer_password = "weekend123"
    
    print(f"🔐 Testing authentication for: {weekend_farmer_email}")
    
    # Test authentication
    auth_result = db_manager.authenticate_user(weekend_farmer_email, weekend_farmer_password)
    
    if auth_result:
        print("✅ Weekend farmer authentication successful!")
        print(f"   User ID: {auth_result['id']}")
        print(f"   Name: {auth_result['name']}")
        print(f"   Role: {auth_result['role']}")
        print(f"   Location: {auth_result.get('address', 'Not set')}")
    else:
        print("❌ Weekend farmer authentication failed!")

def test_google_api_integration():
    """Test Google API integration specifically"""
    print("\n=== Testing Google API Integration ===")
    
    # Test API key validation
    google_maps_api_key = 'AIzaSyD8HeI8o-c1NXmY7EZ_W7HhbpqOgO_xTLo'
    
    # Try a simple coordinate lookup
    test_location = "Bangalore, Karnataka, India"
    print(f"🔍 Testing coordinate lookup for: {test_location}")
    
    coords = get_location_coordinates(test_location)
    if coords[0] and coords[1]:
        print(f"✅ Coordinate lookup successful: {coords[0]:.4f}, {coords[1]:.4f}")
        
        # Test distance to a nearby location
        nearby_location = "Electronic City, Bangalore, India"
        print(f"📏 Testing distance calculation to: {nearby_location}")
        
        distance_result = calculate_distance(test_location, nearby_location, google_maps_api_key)
        
        if distance_result['success']:
            print(f"✅ Distance calculation successful!")
            print(f"   Distance: {distance_result['distance_text']}")
            print(f"   Duration: {distance_result['duration_text']}")
            print(f"   Method: {distance_result['method']}")
        else:
            print(f"❌ Distance calculation failed: {distance_result.get('error', 'Unknown error')}")
    else:
        print("❌ Coordinate lookup failed!")

def main():
    """Run all tests"""
    print("🚀 Starting Weekend Farming Distance System Tests")
    print("=" * 60)
    
    try:
        # Run tests
        test_google_api_integration()
        test_distance_calculation()
        test_database_operations()
        test_weekend_farmer_authentication()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed! Check the output above for any issues.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
