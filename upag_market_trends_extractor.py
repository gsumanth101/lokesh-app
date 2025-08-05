#!/usr/bin/env python3
"""
UPAG Market Trends Data Extractor
Extracts agricultural market trends data from https://upag.gov.in/
"""

import time
import json
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

class UPAGMarketTrendsExtractor:
    def __init__(self, headless=False):
        """Initialize the extractor with Chrome driver"""
        self.driver = None
        self.headless = headless
        self.data = []
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            print("Chrome driver initialized successfully")
        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
            raise
    
    def navigate_to_upag(self):
        """Navigate to UPAG website and wait for it to load"""
        try:
            print("Navigating to UPAG website...")
            self.driver.get("https://upag.gov.in/")
            
            # Wait for the page to load completely
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for React app to load
            time.sleep(10)
            
            print("Page loaded successfully")
            return True
            
        except TimeoutException:
            print("Timeout waiting for page to load")
            return False
        except Exception as e:
            print(f"Error navigating to UPAG: {e}")
            return False
    
    def find_market_trends_section(self):
        """Find and click on market trends or related sections"""
        try:
            print("Looking for market trends section...")
            
            # Common selectors for market trends, prices, or statistics
            selectors = [
                "//a[contains(text(), 'Market')]",
                "//a[contains(text(), 'Price')]",
                "//a[contains(text(), 'Trend')]",
                "//a[contains(text(), 'Statistics')]",
                "//button[contains(text(), 'Market')]",
                "//button[contains(text(), 'Price')]",
                "//div[contains(text(), 'Market')]",
                "//span[contains(text(), 'Market')]",
                "[data-testid*='market']",
                "[class*='market']",
                "[class*='price']",
                "[class*='trend']"
            ]
            
            for selector in selectors:
                try:
                    if selector.startswith("//"):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        print(f"Found potential market section with selector: {selector}")
                        element = elements[0]
                        self.driver.execute_script("arguments[0].scrollIntoView();", element)
                        time.sleep(2)
                        element.click()
                        time.sleep(5)
                        return True
                        
                except Exception as e:
                    continue
            
            print("No market trends section found with standard selectors")
            return False
            
        except Exception as e:
            print(f"Error finding market trends section: {e}")
            return False
    
    def extract_page_data(self):
        """Extract all available data from current page"""
        try:
            print("Extracting data from current page...")
            
            # Get page source and extract text content
            page_source = self.driver.page_source
            
            # Look for tables, charts, or data containers
            data_elements = []
            
            # Check for tables
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            for table in tables:
                try:
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    table_data = []
                    for row in rows:
                        cells = row.find_elements(By.TAG_NAME, "td") + row.find_elements(By.TAG_NAME, "th")
                        row_data = [cell.text.strip() for cell in cells if cell.text.strip()]
                        if row_data:
                            table_data.append(row_data)
                    
                    if table_data:
                        data_elements.append({
                            "type": "table",
                            "data": table_data,
                            "timestamp": datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            # Check for list items or data containers
            containers = self.driver.find_elements(By.CSS_SELECTOR, 
                "div[class*='data'], div[class*='chart'], div[class*='price'], div[class*='market'], ul, ol")
            
            for container in containers:
                try:
                    text_content = container.text.strip()
                    if text_content and len(text_content) > 10:  # Filter out empty or very short content
                        data_elements.append({
                            "type": "container",
                            "content": text_content,
                            "class": container.get_attribute("class"),
                            "timestamp": datetime.now().isoformat()
                        })
                except Exception as e:
                    continue
            
            return data_elements
            
        except Exception as e:
            print(f"Error extracting page data: {e}")
            return []
    
    def check_for_apis(self):
        """Check network tab for API calls that might contain market data"""
        try:
            print("Checking for API calls...")
            
            # Get browser logs (network requests)
            logs = self.driver.get_log('performance')
            api_calls = []
            
            for log in logs:
                message = json.loads(log['message'])
                if message['message']['method'] == 'Network.responseReceived':
                    url = message['message']['params']['response']['url']
                    if any(keyword in url.lower() for keyword in ['api', 'data', 'market', 'price', 'trend']):
                        api_calls.append(url)
            
            # Try to fetch data from discovered API endpoints
            for api_url in api_calls:
                try:
                    print(f"Trying API endpoint: {api_url}")
                    response = requests.get(api_url, timeout=10)
                    if response.status_code == 200:
                        try:
                            api_data = response.json()
                            if api_data:
                                self.data.append({
                                    "type": "api_data",
                                    "url": api_url,
                                    "data": api_data,
                                    "timestamp": datetime.now().isoformat()
                                })
                        except:
                            # If not JSON, save as text
                            if len(response.text) > 50:
                                self.data.append({
                                    "type": "api_text",
                                    "url": api_url,
                                    "data": response.text,
                                    "timestamp": datetime.now().isoformat()
                                })
                except Exception as e:
                    print(f"Error fetching API data from {api_url}: {e}")
                    continue
            
            return len(api_calls)
            
        except Exception as e:
            print(f"Error checking for APIs: {e}")
            return 0
    
    def explore_navigation(self):
        """Explore navigation menu and click on relevant sections"""
        try:
            print("Exploring navigation menu...")
            
            # Look for navigation menus
            nav_selectors = [
                "nav", "ul[class*='nav']", "div[class*='nav']", 
                "ul[class*='menu']", "div[class*='menu']"
            ]
            
            for selector in nav_selectors:
                try:
                    nav_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for nav in nav_elements:
                        links = nav.find_elements(By.TAG_NAME, "a")
                        buttons = nav.find_elements(By.TAG_NAME, "button")
                        
                        all_clickable = links + buttons
                        
                        for element in all_clickable:
                            text = element.text.lower()
                            if any(keyword in text for keyword in 
                                   ['market', 'price', 'trend', 'statistics', 'data', 'dashboard']):
                                try:
                                    print(f"Clicking on: {element.text}")
                                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
                                    time.sleep(2)
                                    element.click()
                                    time.sleep(5)
                                    
                                    # Extract data from this page
                                    page_data = self.extract_page_data()
                                    if page_data:
                                        self.data.extend(page_data)
                                    
                                    return True
                                    
                                except Exception as e:
                                    print(f"Error clicking element: {e}")
                                    continue
                
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error exploring navigation: {e}")
            return False
    
    def extract_all_text_content(self):
        """Extract all text content from the page as fallback"""
        try:
            print("Extracting all text content as fallback...")
            
            # Get all text content from the page
            body = self.driver.find_element(By.TAG_NAME, "body")
            all_text = body.text
            
            # Filter for lines that might contain market/price data
            lines = all_text.split('\n')
            relevant_lines = []
            
            keywords = ['price', 'market', 'trend', 'rs', '₹', 'quintal', 'kg', 'rate', 'mandi']
            
            for line in lines:
                line = line.strip()
                if line and any(keyword in line.lower() for keyword in keywords):
                    relevant_lines.append(line)
            
            if relevant_lines:
                self.data.append({
                    "type": "text_content",
                    "relevant_lines": relevant_lines,
                    "timestamp": datetime.now().isoformat()
                })
                print(f"Extracted {len(relevant_lines)} relevant lines")
            
            return len(relevant_lines)
            
        except Exception as e:
            print(f"Error extracting text content: {e}")
            return 0
    
    def save_data(self, filename=None):
        """Save extracted data to files"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"upag_market_data_{timestamp}"
        
        try:
            # Save as JSON
            json_file = f"{filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {json_file}")
            
            # Try to save as CSV if possible
            if self.data:
                try:
                    csv_data = []
                    for item in self.data:
                        if item['type'] == 'table' and 'data' in item:
                            for row in item['data']:
                                csv_data.append({
                                    'timestamp': item['timestamp'],
                                    'type': item['type'],
                                    'content': ' | '.join(row) if isinstance(row, list) else str(row)
                                })
                        else:
                            csv_data.append({
                                'timestamp': item.get('timestamp', ''),
                                'type': item.get('type', ''),
                                'content': str(item.get('data', item.get('content', '')))[:500]  # Limit length
                            })
                    
                    if csv_data:
                        df = pd.DataFrame(csv_data)
                        csv_file = f"{filename}.csv"
                        df.to_csv(csv_file, index=False, encoding='utf-8')
                        print(f"Data also saved to {csv_file}")
                        
                except Exception as e:
                    print(f"Could not save as CSV: {e}")
            
            return json_file
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return None
    
    def run_extraction(self):
        """Main extraction process"""
        try:
            print("Starting UPAG market trends extraction...")
            
            # Navigate to website
            if not self.navigate_to_upag():
                return False
            
            # Take screenshot for reference
            self.driver.save_screenshot("upag_homepage.png")
            print("Screenshot saved as upag_homepage.png")
            
            # Try different approaches to find market data
            approaches = [
                self.find_market_trends_section,
                self.explore_navigation,
                self.extract_page_data,
                self.extract_all_text_content
            ]
            
            for approach in approaches:
                try:
                    print(f"Trying approach: {approach.__name__}")
                    result = approach()
                    if result:
                        print(f"Success with approach: {approach.__name__}")
                        # Continue to try other approaches to get more data
                    time.sleep(3)  # Wait between approaches
                except Exception as e:
                    print(f"Error with approach {approach.__name__}: {e}")
                    continue
            
            # Check for API calls
            self.check_for_apis()
            
            # Save all collected data
            if self.data:
                filename = self.save_data()
                print(f"\nExtraction completed! Found {len(self.data)} data items.")
                print(f"Data saved to {filename}")
                
                # Print summary of extracted data
                print("\nData Summary:")
                for i, item in enumerate(self.data[:5]):  # Show first 5 items
                    print(f"{i+1}. Type: {item.get('type', 'Unknown')}")
                    if 'data' in item:
                        data_preview = str(item['data'])[:100] + "..." if len(str(item['data'])) > 100 else str(item['data'])
                        print(f"   Preview: {data_preview}")
                    elif 'content' in item:
                        content_preview = item['content'][:100] + "..." if len(item['content']) > 100 else item['content']
                        print(f"   Content: {content_preview}")
                    print()
                
                return True
            else:
                print("No market trends data found. The website might require login or have different structure.")
                return False
                
        except Exception as e:
            print(f"Error during extraction: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser closed.")

def main():
    """Main function to run the extractor"""
    print("UPAG Market Trends Data Extractor")
    print("=" * 40)
    
    # You can set headless=True to run without opening browser window
    extractor = UPAGMarketTrendsExtractor(headless=False)
    
    try:
        success = extractor.run_extraction()
        if success:
            print("\n✅ Extraction completed successfully!")
        else:
            print("\n❌ Extraction failed or no data found.")
    
    except KeyboardInterrupt:
        print("\n\nExtraction interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    finally:
        if extractor.driver:
            extractor.driver.quit()

if __name__ == "__main__":
    main()
