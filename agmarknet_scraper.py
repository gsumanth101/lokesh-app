"""
Agmarknet Web Scraper for Real-time Crop Market Prices
Built for Smart Farming Application - Live Price Dashboard
"""

import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from dataclasses import dataclass

@dataclass
class MarketPrice:
    """Data structure for market price information"""
    mandi_name: str
    state: str
    district: str
    commodity: str
    variety: str
    arrival_date: str
    min_price: float
    max_price: float
    modal_price: float
    unit: str = "Quintal"

class AgmarknetScraper:
    """
    Advanced web scraper for Agmarknet portal with real-time price extraction
    Handles dynamic content loading and provides comprehensive market data
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        """
        Initialize the scraper with Chrome WebDriver
        
        Args:
            headless: Run browser in headless mode
            timeout: Default timeout for operations
        """
        self.base_url = "https://agmarknet.gov.in"
        self.timeout = timeout
        self.driver = None
        self.headless = headless
        
        # Common crop mappings for better search results
        self.crop_mappings = {
            'rice': ['Rice', 'Paddy', 'Basmati Rice'],
            'wheat': ['Wheat', 'Wheat (Dara)', 'Wheat (Average)'],
            'maize': ['Maize', 'Corn', 'Maize (Hybrid)'],
            'cotton': ['Cotton', 'Cotton (Kapas)', 'Cotton (MCU-5)'],
            'sugarcane': ['Sugarcane', 'Sugar Cane'],
            'potato': ['Potato', 'Potato (Medium)'],
            'onion': ['Onion', 'Onion (Big)', 'Onion (Medium)'],
            'tomato': ['Tomato', 'Tomato (Big)', 'Tomato (Medium)'],
            'apple': ['Apple', 'Apple (Indian)'],
            'banana': ['Banana', 'Banana (Ripe)']
        }
        
        # State mappings for accurate selection
        self.state_mappings = {
            'andhra pradesh': 'Andhra Pradesh',
            'telangana': 'Telangana',
            'karnataka': 'Karnataka',
            'tamil nadu': 'Tamil Nadu',
            'kerala': 'Kerala',
            'maharashtra': 'Maharashtra',
            'gujarat': 'Gujarat',
            'rajasthan': 'Rajasthan',
            'punjab': 'Punjab',
            'haryana': 'Haryana',
            'uttar pradesh': 'Uttar Pradesh',
            'bihar': 'Bihar',
            'west bengal': 'West Bengal',
            'odisha': 'Odisha',
            'madhya pradesh': 'Madhya Pradesh',
            'chhattisgarh': 'Chhattisgarh'
        }
        
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('AgmarknetScraper')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _init_driver(self) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with optimized settings"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Optimization flags
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            
            # User agent for better compatibility
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            
            # Initialize driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.implicitly_wait(10)
            
            self.logger.info("Chrome WebDriver initialized successfully")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise
    
    def get_market_prices(self, crop: str, state: str, date: str = None) -> List[MarketPrice]:
        """
        Fetch real-time market prices for specified crop and state
        
        Args:
            crop: Crop name (e.g., 'rice', 'wheat')
            state: State name (e.g., 'telangana', 'punjab')
            date: Date in YYYY-MM-DD format (defaults to today)
            
        Returns:
            List of MarketPrice objects with pricing data
        """
        if not self.driver:
            self._init_driver()
        
        try:
            # Format inputs
            crop_name = self._get_crop_name(crop.lower())
            state_name = self._get_state_name(state.lower())
            target_date = date or datetime.now().strftime("%Y-%m-%d")
            
            self.logger.info(f"Fetching prices for {crop_name} in {state_name} for {target_date}")
            
            # Navigate to commodity report page
            report_url = f"{self.base_url}/SearchCmmMkt.aspx"
            self.driver.get(report_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.ID, "ddlCommodity"))
            )
            
            # Select commodity
            self._select_commodity(crop_name)
            
            # Select state
            self._select_state(state_name)
            
            # Set date
            self._set_date(target_date)
            
            # Submit search
            self._submit_search()
            
            # Extract price data
            price_data = self._extract_price_table()
            
            self.logger.info(f"Successfully extracted {len(price_data)} price records")
            return price_data
            
        except Exception as e:
            self.logger.error(f"Error fetching market prices: {str(e)}")
            return []
    
    def _get_crop_name(self, crop: str) -> str:
        """Get standardized crop name for Agmarknet"""
        crop = crop.lower().strip()
        if crop in self.crop_mappings:
            return self.crop_mappings[crop][0]  # Return primary mapping
        return crop.title()

def get_sample_market_data():
    """Generate sample market data for testing/fallback purposes"""
    import random
    from datetime import datetime
    
    sample_data = [
        MarketPrice(
            mandi_name="Kurnool Market",
            state="Andhra Pradesh",
            district="Kurnool",
            commodity="Rice",
            variety="Common",
            arrival_date=datetime.now().strftime("%Y-%m-%d"),
            min_price=2000.0 + random.uniform(-200, 200),
            max_price=2500.0 + random.uniform(-200, 200),
            modal_price=2250.0 + random.uniform(-200, 200),
            unit="Quintal"
        ),
        MarketPrice(
            mandi_name="Hyderabad Market",
            state="Telangana",
            district="Hyderabad",
            commodity="Wheat",
            variety="Dara",
            arrival_date=datetime.now().strftime("%Y-%m-%d"),
            min_price=1800.0 + random.uniform(-150, 150),
            max_price=2200.0 + random.uniform(-150, 150),
            modal_price=2000.0 + random.uniform(-150, 150),
            unit="Quintal"
        ),
        MarketPrice(
            mandi_name="Bangalore Market",
            state="Karnataka",
            district="Bangalore",
            commodity="Tomato",
            variety="Big",
            arrival_date=datetime.now().strftime("%Y-%m-%d"),
            min_price=800.0 + random.uniform(-100, 100),
            max_price=1200.0 + random.uniform(-100, 100),
            modal_price=1000.0 + random.uniform(-100, 100),
            unit="Quintal"
        ),
        MarketPrice(
            mandi_name="Mumbai Market",
            state="Maharashtra",
            district="Mumbai",
            commodity="Cotton",
            variety="Medium",
            arrival_date=datetime.now().strftime("%Y-%m-%d"),
            min_price=5000.0 + random.uniform(-300, 300),
            max_price=5800.0 + random.uniform(-300, 300),
            modal_price=5400.0 + random.uniform(-300, 300),
            unit="Quintal"
        ),
        MarketPrice(
            mandi_name="Ludhiana Market",
            state="Punjab",
            district="Ludhiana",
            commodity="Maize",
            variety="Hybrid",
            arrival_date=datetime.now().strftime("%Y-%m-%d"),
            min_price=1600.0 + random.uniform(-120, 120),
            max_price=1900.0 + random.uniform(-120, 120),
            modal_price=1750.0 + random.uniform(-120, 120),
            unit="Quintal"
        )
    ]
    
    return sample_data
    
    def _get_state_name(self, state: str) -> str:
        """Get standardized state name for Agmarknet"""
        state = state.lower().strip()
        return self.state_mappings.get(state, state.title())
    
    def _select_commodity(self, crop_name: str):
        """Select commodity from dropdown"""
        try:
            commodity_dropdown = Select(self.driver.find_element(By.ID, "ddlCommodity"))
            
            # Try to find exact match first
            for option in commodity_dropdown.options:
                if crop_name.lower() in option.text.lower():
                    commodity_dropdown.select_by_visible_text(option.text)
                    self.logger.info(f"Selected commodity: {option.text}")
                    return
            
            # If no exact match, try partial match
            for option in commodity_dropdown.options:
                if any(word in option.text.lower() for word in crop_name.lower().split()):
                    commodity_dropdown.select_by_visible_text(option.text)
                    self.logger.info(f"Selected commodity (partial match): {option.text}")
                    return
            
            self.logger.warning(f"Commodity '{crop_name}' not found, using first available option")
            commodity_dropdown.select_by_index(1)  # Skip "Select" option
            
        except Exception as e:
            self.logger.error(f"Error selecting commodity: {str(e)}")
            raise
    
    def _select_state(self, state_name: str):
        """Select state from dropdown"""
        try:
            # Wait for state dropdown to be populated after commodity selection
            time.sleep(2)
            
            state_dropdown = Select(self.driver.find_element(By.ID, "ddlState"))
            
            # Try to find exact match
            for option in state_dropdown.options:
                if state_name.lower() == option.text.lower():
                    state_dropdown.select_by_visible_text(option.text)
                    self.logger.info(f"Selected state: {option.text}")
                    return
            
            # Try partial match
            for option in state_dropdown.options:
                if state_name.lower() in option.text.lower():
                    state_dropdown.select_by_visible_text(option.text)
                    self.logger.info(f"Selected state (partial match): {option.text}")
                    return
            
            self.logger.warning(f"State '{state_name}' not found, using first available option")
            state_dropdown.select_by_index(1)  # Skip "Select" option
            
        except Exception as e:
            self.logger.error(f"Error selecting state: {str(e)}")
            raise
    
    def _set_date(self, date_str: str):
        """Set the date for price query"""
        try:
            date_input = self.driver.find_element(By.ID, "txtDate")
            date_input.clear()
            
            # Convert date format if needed (YYYY-MM-DD to DD/MM/YYYY)
            if "-" in date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d/%m/%Y")
            else:
                formatted_date = date_str
            
            date_input.send_keys(formatted_date)
            self.logger.info(f"Set date to: {formatted_date}")
            
        except Exception as e:
            self.logger.error(f"Error setting date: {str(e)}")
            # Continue without specific date (will use default)
    
    def _submit_search(self):
        """Submit the search form"""
        try:
            search_button = self.driver.find_element(By.ID, "btnSubmit")
            search_button.click()
            
            # Wait for results to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            self.logger.info("Search submitted successfully")
            
        except Exception as e:
            self.logger.error(f"Error submitting search: {str(e)}")
            raise
    
    def _extract_price_table(self) -> List[MarketPrice]:
        """Extract price data from results table"""
        prices = []
        
        try:
            # Find the main data table
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            
            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                if len(rows) < 2:  # Skip tables without data rows
                    continue
                
                # Check if this is the price data table
                header_row = rows[0]
                headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, "th")]
                
                if not any(keyword in ' '.join(headers).lower() 
                          for keyword in ['mandi', 'price', 'min', 'max', 'modal']):
                    continue
                
                # Extract data from each row
                for row in rows[1:]:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    if len(cells) < 6:  # Skip incomplete rows
                        continue
                    
                    try:
                        price_info = MarketPrice(
                            mandi_name=cells[1].text.strip() if len(cells) > 1 else "Unknown",
                            state=cells[0].text.strip() if len(cells) > 0 else "Unknown",
                            district=cells[2].text.strip() if len(cells) > 2 else "Unknown",
                            commodity=cells[3].text.strip() if len(cells) > 3 else "Unknown",
                            variety=cells[4].text.strip() if len(cells) > 4 else "Unknown",
                            arrival_date=cells[5].text.strip() if len(cells) > 5 else datetime.now().strftime("%d/%m/%Y"),
                            min_price=self._parse_price(cells[6].text if len(cells) > 6 else "0"),
                            max_price=self._parse_price(cells[7].text if len(cells) > 7 else "0"),
                            modal_price=self._parse_price(cells[8].text if len(cells) > 8 else "0")
                        )
                        
                        # Only add if we have valid price data
                        if price_info.modal_price > 0:
                            prices.append(price_info)
                            
                    except Exception as e:
                        self.logger.warning(f"Error parsing price row: {str(e)}")
                        continue
                
                # If we found data in this table, break
                if prices:
                    break
            
            return prices
            
        except Exception as e:
            self.logger.error(f"Error extracting price table: {str(e)}")
            return []
    
    def _parse_price(self, price_str: str) -> float:
        """Parse price string to float value"""
        try:
            # Remove currency symbols, commas, and extra spaces
            cleaned = price_str.replace('₹', '').replace(',', '').strip()
            
            # Handle cases like "2000-2500" (take average)
            if '-' in cleaned:
                parts = cleaned.split('-')
                if len(parts) == 2:
                    try:
                        return (float(parts[0]) + float(parts[1])) / 2
                    except:
                        pass
            
            # Convert to float
            return float(cleaned) if cleaned else 0.0
            
        except (ValueError, AttributeError):
            return 0.0
    
    def get_price_trends(self, crop: str, state: str, days: int = 7) -> Dict:
        """
        Get price trends over multiple days
        
        Args:
            crop: Crop name
            state: State name
            days: Number of days to fetch (default 7)
            
        Returns:
            Dictionary with trend data and analytics
        """
        trends = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_prices = self.get_market_prices(crop, state, date)
            
            if daily_prices:
                avg_modal = sum(p.modal_price for p in daily_prices) / len(daily_prices)
                trends.append({
                    'date': date,
                    'avg_price': avg_modal,
                    'records_count': len(daily_prices),
                    'price_data': daily_prices
                })
        
        # Calculate trend analytics
        if len(trends) >= 2:
            current_price = trends[0]['avg_price']
            previous_price = trends[1]['avg_price']
            price_change = current_price - previous_price
            price_change_percent = (price_change / previous_price) * 100 if previous_price > 0 else 0
            
            return {
                'trends': trends,
                'analytics': {
                    'current_avg_price': current_price,
                    'price_change': price_change,
                    'price_change_percent': price_change_percent,
                    'trend_direction': 'up' if price_change > 0 else 'down' if price_change < 0 else 'stable'
                }
            }
        
        return {'trends': trends, 'analytics': {}}
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed successfully")

def get_sample_market_data() -> List[MarketPrice]:
    """
    Generate sample market data for testing purposes
    Returns realistic sample data when scraper is unavailable
    """
    sample_data = [
        MarketPrice(
            mandi_name="Hyderabad",
            state="Telangana",
            district="Hyderabad",
            commodity="Rice",
            variety="Sona Masuri",
            arrival_date=datetime.now().strftime("%d/%m/%Y"),
            min_price=2800.0,
            max_price=3200.0,
            modal_price=3000.0
        ),
        MarketPrice(
            mandi_name="Warangal",
            state="Telangana", 
            district="Warangal",
            commodity="Rice",
            variety="BPT 5204",
            arrival_date=datetime.now().strftime("%d/%m/%Y"),
            min_price=2700.0,
            max_price=3100.0,
            modal_price=2900.0
        ),
        MarketPrice(
            mandi_name="Nizamabad",
            state="Telangana",
            district="Nizamabad",
            commodity="Rice",
            variety="IR 64",
            arrival_date=datetime.now().strftime("%d/%m/%Y"),
            min_price=2750.0,
            max_price=3150.0,
            modal_price=2950.0
        )
    ]
    
    return sample_data

if __name__ == "__main__":
    # Test the scraper
    scraper = AgmarknetScraper(headless=True)
    
    try:
        prices = scraper.get_market_prices("rice", "telangana")
        
        if prices:
            print(f"\nFound {len(prices)} price records:")
            for price in prices[:3]:  # Show first 3 records
                print(f"Mandi: {price.mandi_name}, Modal Price: ₹{price.modal_price}/quintal")
        else:
            print("No price data found, using sample data")
            sample_prices = get_sample_market_data()
            for price in sample_prices:
                print(f"Mandi: {price.mandi_name}, Modal Price: ₹{price.modal_price}/quintal")
                
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        scraper.close()
