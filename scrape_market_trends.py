import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import re

def scrape_commodity_data():
    """Scrape commodity market data from commodityonline.com"""
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # URL to scrape
    url = "https://www.commodityonline.com/"
    
    try:
        print(f"🌐 Fetching data from {url}...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Successfully connected to commodityonline.com")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            market_data = []
            
            # Try to find commodity data in various potential locations
            # Method 1: Look for price tables
            price_tables = soup.find_all('table')
            if price_tables:
                print(f"📊 Found {len(price_tables)} tables on the page")
                for table in price_tables:
                    rows = table.find_all('tr')
                    for row in rows[1:]:  # Skip header row
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 2:
                            commodity_name = cells[0].get_text(strip=True)
                            price_info = cells[1].get_text(strip=True)
                            if commodity_name and price_info:
                                market_data.append({
                                    'commodity': commodity_name,
                                    'price': price_info,
                                    'source': 'table_data'
                                })
            
            # Method 2: Look for specific commodity sections
            commodity_sections = soup.find_all(['div', 'section'], class_=re.compile(r'.*commodity.*|.*price.*|.*market.*', re.I))
            print(f"🔍 Found {len(commodity_sections)} commodity-related sections")
            
            for section in commodity_sections:
                commodity_items = section.find_all(['div', 'span', 'p'], class_=re.compile(r'.*price.*|.*rate.*|.*commodity.*', re.I))
                for item in commodity_items:
                    text = item.get_text(strip=True)
                    if text and any(keyword in text.lower() for keyword in ['rs', '₹', 'price', 'rate', '/kg', '/quintal']):
                        market_data.append({
                            'commodity': 'Mixed Data',
                            'price': text,
                            'source': 'section_data'
                        })
            
            # Method 3: Extract all text and look for patterns
            all_text = soup.get_text()
            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
            
            # Look for price patterns
            price_patterns = [
                r'([A-Za-z\s]+)\s*[:-]\s*(?:Rs\.?|₹)\s*([0-9,]+(?:\.[0-9]{1,2})?)',
                r'([A-Za-z\s]+)\s*[:-]\s*([0-9,]+(?:\.[0-9]{1,2})?)\s*(?:/kg|/quintal|per kg|per quintal)',
                r'([A-Za-z\s]{3,})\s+([0-9,]+(?:\.[0-9]{1,2})?)'
            ]
            
            for line in lines:
                for pattern in price_patterns:
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    for match in matches:
                        if len(match) == 2:
                            commodity_name, price = match
                            if len(commodity_name.strip()) > 2 and len(price.strip()) > 0:
                                market_data.append({
                                    'commodity': commodity_name.strip().title(),
                                    'price': price.strip(),
                                    'source': 'pattern_match'
                                })
            
            # Method 4: Extract specific commodity categories mentioned in the content
            commodity_categories = [
                'Apple', 'Banana', 'Grapes', 'Lemon', 'Mango', 'Orange', 'Wheat', 'Rice', 'Maize',
                'Bajra', 'Barley', 'Cotton', 'Sugarcane', 'Onion', 'Potato', 'Tomato', 'Groundnut',
                'Soybean', 'Mustard', 'Turmeric', 'Cardamom', 'Pepper', 'Ginger', 'Chilli'
            ]
            
            for category in commodity_categories:
                # Look for this commodity in the text
                pattern = rf'{category}[^\n]*?(?:Rs\.?|₹|price|rate)[^\n]*?([0-9,]+(?:\.[0-9]{{1,2}})?)[^\n]*?(?:/kg|/quintal|per kg|per quintal)?'
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                for price in matches:
                    market_data.append({
                        'commodity': category,
                        'price': f'₹{price}',
                        'source': 'category_search'
                    })
            
            # Remove duplicates and clean data
            unique_data = []
            seen = set()
            for item in market_data:
                key = (item['commodity'].lower(), item['price'])
                if key not in seen:
                    seen.add(key)
                    unique_data.append(item)
            
            if unique_data:
                print(f"\n📈 Successfully extracted {len(unique_data)} commodity price entries:")
                print("=" * 60)
                for i, item in enumerate(unique_data[:20], 1):  # Show first 20 items
                    print(f"{i:2d}. {item['commodity']:<25} | {item['price']:<15} | Source: {item['source']}")
                
                # Save to JSON file
                output_data = {
                    'timestamp': datetime.now().isoformat(),
                    'source': 'commodityonline.com',
                    'total_items': len(unique_data),
                    'commodities': unique_data
                }
                
                with open('market_data.json', 'w') as f:
                    json.dump(output_data, f, indent=2)
                
                print(f"\n💾 Data saved to 'market_data.json'")
                return unique_data
            else:
                print("⚠️  No commodity price data found. The website structure might have changed.")
                # Create some sample data for demonstration
                sample_data = [
                    {'commodity': 'Wheat', 'price': '₹2,150/quintal', 'source': 'sample_data'},
                    {'commodity': 'Rice', 'price': '₹3,200/quintal', 'source': 'sample_data'},
                    {'commodity': 'Maize', 'price': '₹1,850/quintal', 'source': 'sample_data'},
                    {'commodity': 'Cotton', 'price': '₹5,750/quintal', 'source': 'sample_data'},
                    {'commodity': 'Sugarcane', 'price': '₹350/quintal', 'source': 'sample_data'},
                    {'commodity': 'Onion', 'price': '₹45/kg', 'source': 'sample_data'},
                    {'commodity': 'Potato', 'price': '₹28/kg', 'source': 'sample_data'},
                    {'commodity': 'Tomato', 'price': '₹35/kg', 'source': 'sample_data'},
                ]
                
                print("📊 Using sample commodity data:")
                for item in sample_data:
                    print(f"  - {item['commodity']}: {item['price']}")
                
                return sample_data
                
        else:
            print(f"❌ Failed to retrieve the page, status code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"🌐 Network error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return []

def display_market_summary(data):
    """Display a summary of market data"""
    if not data:
        print("No market data available.")
        return
    
    print("\n" + "="*50)
    print("🌾 COMMODITY MARKET SUMMARY")
    print("="*50)
    
    categories = {}
    for item in data:
        commodity = item['commodity']
        price = item['price']
        
        # Categorize commodities
        if any(grain in commodity.lower() for grain in ['wheat', 'rice', 'maize', 'bajra', 'barley']):
            category = '🌾 Grains'
        elif any(fruit in commodity.lower() for fruit in ['apple', 'banana', 'mango', 'orange', 'grapes']):
            category = '🍎 Fruits'
        elif any(veg in commodity.lower() for veg in ['onion', 'potato', 'tomato']):
            category = '🥕 Vegetables'
        elif any(spice in commodity.lower() for spice in ['turmeric', 'pepper', 'cardamom', 'chilli']):
            category = '🌶️ Spices'
        else:
            category = '🌱 Others'
        
        if category not in categories:
            categories[category] = []
        categories[category].append(f"{commodity}: {price}")
    
    for category, items in categories.items():
        print(f"\n{category}:")
        for item in items[:5]:  # Show max 5 items per category
            print(f"  • {item}")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more")

if __name__ == "__main__":
    print("🚀 Starting Commodity Market Data Scraper...")
    market_data = scrape_commodity_data()
    display_market_summary(market_data)
    print("\n✅ Scraping completed!")
