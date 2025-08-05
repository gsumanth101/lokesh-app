#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def scrape_commodity_online():
    """
    Scrape market data from Commodity Online website
    """
    try:
        url = "https://www.commodityonline.com/"
        
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print("🌐 Fetching data from Commodity Online...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"✅ Successfully fetched page (Status: {response.status_code})")
            print(f"📄 Page title: {soup.title.text if soup.title else 'No title found'}")
            
            # Try to find commodity data in various possible structures
            market_data = []
            
            # Method 1: Look for table structures
            tables = soup.find_all('table')
            if tables:
                print(f"📊 Found {len(tables)} tables")
                for i, table in enumerate(tables[:3]):  # Check first 3 tables
                    rows = table.find_all('tr')
                    if len(rows) > 1:  # Has header and data rows
                        print(f"  Table {i+1}: {len(rows)} rows")
                        
            # Method 2: Look for commodity price divs/spans
            price_elements = soup.find_all(['div', 'span'], class_=re.compile(r'price|commodity|market', re.I))
            if price_elements:
                print(f"💰 Found {len(price_elements)} potential price elements")
                
            # Method 3: Look for common commodity names
            commodities = ['wheat', 'rice', 'corn', 'soybean', 'cotton', 'sugar', 'gold', 'silver', 'crude', 'copper']
            
            for commodity in commodities:
                # Search for commodity mentions in the page
                commodity_mentions = soup.find_all(text=re.compile(commodity, re.I))
                if commodity_mentions:
                    print(f"🌾 Found mentions of '{commodity}': {len(commodity_mentions)}")
                    
                    # Try to find associated price data
                    for mention in commodity_mentions[:2]:  # Check first 2 mentions
                        parent = mention.parent
                        if parent:
                            # Look for price patterns in nearby text
                            parent_text = parent.get_text()
                            price_match = re.search(r'[\$₹]?\s*\d+[\.,]?\d*', parent_text)
                            if price_match:
                                market_data.append({
                                    'commodity': commodity.title(),
                                    'price': price_match.group().strip(),
                                    'context': parent_text.strip()[:100],
                                    'timestamp': datetime.now().isoformat()
                                })
            
            # Method 4: Look for structured data (JSON-LD, etc.)
            json_scripts = soup.find_all('script', type='application/ld+json')
            if json_scripts:
                print(f"📋 Found {len(json_scripts)} JSON-LD scripts")
                for script in json_scripts:
                    try:
                        data = json.loads(script.string)
                        # Process structured data if relevant
                        if isinstance(data, dict) and any(key in str(data).lower() for key in ['price', 'commodity', 'market']):
                            print("💡 Found relevant structured data")
                    except:
                        pass
            
            # Method 5: Generic content extraction
            if not market_data:
                # Look for any numerical data that might be prices
                all_text = soup.get_text()
                price_patterns = re.findall(r'[\$₹]\s*\d+[\.,]?\d*|\d+[\.,]?\d*\s*(?:per|/)\s*\w+', all_text)
                
                if price_patterns:
                    print(f"🔍 Found {len(price_patterns)} potential price patterns")
                    for i, pattern in enumerate(price_patterns[:10]):  # Show first 10
                        market_data.append({
                            'commodity': f'Item {i+1}',
                            'price': pattern.strip(),
                            'source': 'pattern_match',
                            'timestamp': datetime.now().isoformat()
                        })
            
            return {
                'success': True,
                'data': market_data,
                'total_items': len(market_data),
                'source': 'commodityonline.com',
                'scraped_at': datetime.now().isoformat()
            }
            
        else:
            return {
                'success': False,
                'error': f'HTTP {response.status_code}',
                'message': 'Failed to fetch page'
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': 'Network Error',
            'message': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': 'Parsing Error',
            'message': str(e)
        }

def display_market_data(data):
    """Display scraped market data in a formatted way"""
    if data['success']:
        print(f"\n📈 Market Data Summary")
        print(f"{'='*50}")
        print(f"Source: {data['source']}")
        print(f"Total Items: {data['total_items']}")
        print(f"Scraped At: {data['scraped_at']}")
        print(f"{'='*50}")
        
        if data['data']:
            for i, item in enumerate(data['data'], 1):
                print(f"\n{i}. {item['commodity']}")
                print(f"   Price: {item['price']}")
                if 'context' in item:
                    print(f"   Context: {item['context']}")
                print(f"   Timestamp: {item['timestamp']}")
        else:
            print("No market data found.")
    else:
        print(f"❌ Error: {data['error']}")
        print(f"Message: {data['message']}")

if __name__ == "__main__":
    print("🚀 Starting Commodity Online Market Data Scraper")
    print("="*60)
    
    # Scrape the data
    result = scrape_commodity_online()
    
    # Display results
    display_market_data(result)
    
    # Save to file
    with open('market_data.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Data saved to market_data.json")
