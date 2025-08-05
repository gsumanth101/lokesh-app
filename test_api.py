#!/usr/bin/env python3
"""
Test API and create new market trends service
"""

import requests
import json

def test_market_api():
    """Test the provided API key for market data"""
    
    api_key = "579b464db66ec23bdd000001ba21a1d30966476a7f19d8adf57ef501"
    
    # Common market data API endpoints to try
    possible_apis = [
        {
            'name': 'Data.gov.in Agriculture API',
            'url': 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070',
            'params': {'api-key': api_key, 'format': 'json', 'limit': 10}
        },
        {
            'name': 'Data.gov.in Market Prices API',
            'url': 'https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24',
            'params': {'api-key': api_key, 'format': 'json', 'limit': 10}
        },
        {
            'name': 'Data.gov.in Commodity Prices',
            'url': 'https://api.data.gov.in/resource/fea6c845-8b02-4cee-84f3-bc7d4e5e9354',
            'params': {'api-key': api_key, 'format': 'json', 'limit': 10}
        },
        {
            'name': 'Data.gov.in Agricultural Market Prices',  
            'url': 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070',
            'params': {'api-key': api_key, 'format': 'json', 'limit': 5}
        }
    ]
    
    print("Testing API key with different endpoints...\n")
    
    for api_info in possible_apis:
        try:
            print(f"Testing: {api_info['name']}")
            print(f"URL: {api_info['url']}")
            
            response = requests.get(api_info['url'], params=api_info['params'], timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ SUCCESS! API response received")
                    print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'List response'}")
                    
                    if isinstance(data, dict) and 'records' in data:
                        records = data['records']
                        print(f"Number of records: {len(records)}")
                        if records:
                            print("Sample record keys:", list(records[0].keys()))
                            print("Sample record:", json.dumps(records[0], indent=2)[:500] + "...")
                    elif isinstance(data, list) and data:
                        print(f"Number of items: {len(data)}")
                        print("Sample item keys:", list(data[0].keys()) if data else "No data")
                        
                    return api_info, data
                    
                except json.JSONDecodeError:
                    print("Response is not valid JSON")
                    print("Raw response:", response.text[:200] + "...")
            else:
                print(f"❌ Failed with status {response.status_code}")
                print("Response:", response.text[:200] + "...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            
        print("-" * 50)
    
    return None, None

if __name__ == "__main__":
    api_info, data = test_market_api()
    
    if api_info:
        print(f"\n🎉 Successfully identified API: {api_info['name']}")
        print("This API will be used for the market trends service.")
    else:
        print("\n❌ Could not identify a working API with the provided key.")
        print("Please verify the API key or provide the correct API endpoint.")
