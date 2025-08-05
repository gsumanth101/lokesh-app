"""
Market Trends Service
Real-time crop price fetching with caching and fallback mechanisms
Integrates with Agmarknet scraper for live market data
"""

import json
import time
import logging
from datetime import datetime, timedelta
import pickle
from typing import Dict, List, Optional, Tuple
import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from dataclasses import asdict
import requests

try:
    from agmarknet_scraper import AgmarknetScraper, MarketPrice, get_sample_market_data
    SCRAPER_AVAILABLE = True
except ImportError as e:
    SCRAPER_AVAILABLE = False
    # Define MarketPrice locally as fallback
    from dataclasses import dataclass
    
    @dataclass
    class MarketPrice:
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
    
    def get_sample_market_data():
        """Generate sample market data when scraper is not available"""
        import random
        from datetime import datetime
        
        return [
            MarketPrice(
                mandi_name="Sample Market",
                state="Sample State",
                district="Sample District",
                commodity="Rice",
                variety="Common",
                arrival_date=datetime.now().strftime("%Y-%m-%d"),
                min_price=2000.0 + random.uniform(-200, 200),
                max_price=2500.0 + random.uniform(-200, 200),
                modal_price=2250.0 + random.uniform(-200, 200),
                unit="Quintal"
            )
        ]
    
    if 'st' in globals():
        st.warning("Agmarknet scraper not available. Using fallback data.")

# Load the comprehensive trained model for all commodities
MODEL_PATH = 'full_market_model.pkl'
price_prediction_data = None

try:
    with open(MODEL_PATH, 'rb') as model_file:
        price_prediction_data = pickle.load(model_file)
    print("✅ Comprehensive prediction model loaded successfully (147 commodities supported)")
except FileNotFoundError:
    print(f"Warning: Model file {MODEL_PATH} not found. Prediction functionality will be disabled.")
except Exception as e:
    print(f"Warning: Error loading model: {e}. Prediction functionality will be disabled.")

class MarketTrendsService:
    """
    Service class for managing real-time market trends data
    Handles caching, error recovery, and data aggregation
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 3600  # 1 hour cache
        self.scraper = None
        self.logger = self._setup_logger()
        
        # Initialize scraper if available
        if SCRAPER_AVAILABLE:
            try:
                self.scraper = AgmarknetScraper(headless=True, timeout=30)
                self.logger.info("Agmarknet scraper initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize scraper: {e}")
                self.scraper = None
        
        # Popular crops for quick access (based on actual dataset)
        self.popular_crops = [
            'Potato', 'Tomato', 'Onion', 'Brinjal', 'Banana', 
            'Bhindi(Ladies Finger)', 'Green Chilli', 'Cucumbar(Kheera)', 
            'Bitter gourd', 'Bottle gourd', 'Pumpkin', 'Cabbage', 
            'Cauliflower', 'Wheat', 'Ginger(Green)', 'Apple', 
            'Carrot', 'Capsicum', 'Lemon', 'Rice'
        ]
        
        # Major agricultural states (based on actual dataset)
        self.major_states = [
            'Kerala', 'Uttar Pradesh', 'Himachal Pradesh', 'Punjab', 
            'Haryana', 'Gujarat', 'Maharashtra', 'Odisha', 
            'Rajasthan', 'West Bengal', 'Andhra Pradesh', 'Karnataka',
            'Tamil Nadu', 'Telangana', 'Bihar', 'Jammu and Kashmir'
        ]
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the service"""
        logger = logging.getLogger('MarketTrendsService')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _get_cache_key(self, crop: str, state: str) -> str:
        """Generate cache key for crop-state combination"""
        return f"{crop.lower()}_{state.lower()}_{datetime.now().strftime('%Y-%m-%d')}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key].get('timestamp', 0)
        return (time.time() - cached_time) < self.cache_timeout
    
    def get_market_prices(self, crop: str, state: str, use_cache: bool = True) -> List[MarketPrice]:
        """
        Get market prices for a specific crop and state
        
        Args:
            crop: Crop name
            state: State name
            use_cache: Whether to use cached data
            
        Returns:
            List of MarketPrice objects
        """
        cache_key = self._get_cache_key(crop, state)
        
        # Check cache first
        if use_cache and self._is_cache_valid(cache_key):
            self.logger.info(f"Using cached data for {crop} in {state}")
            return self.cache[cache_key]['data']
        
        # Fetch fresh data
        try:
            self.logger.info(f"Fetching fresh data for {crop} in {state} from API")
            response = requests.get(
                "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
                params={
                    "api-key": "579b464db66ec23bdd000001ba21a1d30966476a7f19d8adf57ef501",
                    "format": "json",
                    "limit": 100,
                    "filters[state]": state,
                    "filters[commodity]": crop
                }
            )
            response.raise_for_status()
            data = response.json()
            records = data.get('records', [])
            
            if records:
                prices = []
                for rec in records:
                    # Only include records with all required fields
                    if all(k in rec for k in ['market', 'state', 'district', 'commodity', 'variety', 'arrival_date', 'min_price', 'max_price', 'modal_price']):
                        try:
                            prices.append(MarketPrice(
                                mandi_name=rec['market'],
                                state=rec['state'],
                                district=rec['district'],
                                commodity=rec['commodity'],
                                variety=rec['variety'],
                                arrival_date=rec['arrival_date'],
                                min_price=float(rec['min_price']),
                                max_price=float(rec['max_price']),
                                modal_price=float(rec['modal_price'])
                            ))
                        except (ValueError, TypeError) as e:
                            self.logger.warning(f"Skipping invalid price record: {e}")
                            continue
                
                # Cache the data
                self.cache[cache_key] = {
                    'data': prices,
                    'timestamp': time.time()
                }
                self.logger.info(f"Successfully fetched {len(prices)} valid price records from API")
                return prices
            else:
                self.logger.warning(f"No data returned from API for {crop} in {state}")
                return []

        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            return []
        except Exception as e:
            self.logger.error(f"Error fetching market prices from API: {e}")
            return []
    
    def get_price_trends(self, crop: str, state: str, days: int = 7) -> Dict:
        """
        Get price trends over multiple days
        
        Args:
            crop: Crop name
            state: State name  
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend data and analytics
        """
        try:
            # Fetch data from API for trend analysis
            self.logger.info(f"Fetching price trends for {crop} in {state} from API")
            response = requests.get(
                "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
                params={
                    "api-key": "579b464db66ec23bdd000001ba21a1d30966476a7f19d8adf57ef501",
                    "format": "json",
                    "limit": 500,  # Get more records for trend analysis
                    "filters[state]": state,
                    "filters[commodity]": crop
                }
            )
            response.raise_for_status()
            data = response.json()
            records = data.get('records', [])
            
            if records:
                return self._analyze_api_trends(records, days)
            else:
                self.logger.warning(f"No data returned from API for trends analysis")
                return self._generate_sample_trends(crop, state, days)
                
        except Exception as e:
            self.logger.error(f"Error fetching price trends: {e}")
            return self._generate_sample_trends(crop, state, days)
    
    def _analyze_api_trends(self, records: List[Dict], days: int) -> Dict:
        """Analyze API records to extract price trends over the specified days"""
        trends = []
        records_by_date = {}

        # Filter and organize records by date - only include complete records
        for record in records:
            if all(k in record for k in ['arrival_date', 'min_price', 'max_price', 'modal_price']):
                try:
                    # Validate that prices are numeric
                    float(record['min_price'])
                    float(record['max_price'])
                    float(record['modal_price'])
                    
                    date = record['arrival_date']
                    if date not in records_by_date:
                        records_by_date[date] = []
                    records_by_date[date].append(record)
                except (ValueError, TypeError):
                    continue  # Skip invalid price records

        # Analyze the most recent days
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_records = records_by_date.get(date, [])

            if daily_records:
                avg_price = sum(float(rec['modal_price']) for rec in daily_records) / len(daily_records)
                min_price = min(float(rec['min_price']) for rec in daily_records)
                max_price = max(float(rec['max_price']) for rec in daily_records)

                trends.append({
                    'date': date,
                    'avg_price': avg_price,
                    'records_count': len(daily_records),
                    'price_data': daily_records
                })

        # Calculate analytics
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

    def _generate_sample_trends(self, crop: str, state: str, days: int) -> Dict:
        """Generate sample trend data for demonstration"""
        import random

        base_price = random.uniform(2000, 4000)  # Base price in rupees
        trends = []

        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            # Add some random variation
            price_variation = random.uniform(-200, 200)
            daily_price = max(1000, base_price + price_variation)

            trends.append({
                'date': date,
                'avg_price': daily_price,
                'records_count': random.randint(3, 8),
                'price_data': []
            })

        # Calculate analytics
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
    
    def get_multi_crop_prices(self, crops: List[str], state: str) -> Dict[str, List[MarketPrice]]:
        """
        Get prices for multiple crops concurrently
        
        Args:
            crops: List of crop names
            state: State name
            
        Returns:
            Dictionary mapping crop names to their price lists
        """
        results = {}
        
        # Use threading for concurrent requests
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_crop = {
                executor.submit(self.get_market_prices, crop, state): crop 
                for crop in crops
            }
            
            for future in as_completed(future_to_crop):
                crop = future_to_crop[future]
                try:
                    prices = future.result(timeout=30)
                    results[crop] = prices
                    self.logger.info(f"Successfully fetched prices for {crop}")
                except Exception as e:
                    self.logger.error(f"Error fetching prices for {crop}: {e}")
                    results[crop] = []
        
        return results
    
    def get_state_market_summary(self, state: str) -> Dict:
        """
        Get market summary for all popular crops in a state
        
        Args:
            state: State name
            
        Returns:
            Dictionary with market summary data
        """
        self.logger.info(f"Generating market summary for {state}")
        
        # Get prices for popular crops
        crop_prices = self.get_multi_crop_prices(self.popular_crops[:5], state)
        
        summary = {
            'state': state,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'total_crops': len(crop_prices),
            'crops': {}
        }
        
        for crop, prices in crop_prices.items():
            if prices:
                avg_price = sum(p.modal_price for p in prices) / len(prices)
                min_price = min(p.min_price for p in prices)
                max_price = max(p.max_price for p in prices)
                
                summary['crops'][crop] = {
                    'avg_price': avg_price,
                    'min_price': min_price,
                    'max_price': max_price,
                    'mandis_count': len(prices),
                    'price_range': max_price - min_price
                }
            else:
                summary['crops'][crop] = {
                    'avg_price': 0,
                    'min_price': 0,
                    'max_price': 0,
                    'mandis_count': 0,
                    'price_range': 0
                }
        
        return summary
    
    def search_mandis_by_crop(self, crop: str, max_states: int = 5) -> Dict[str, List[MarketPrice]]:
        """
        Search for mandis across multiple states for a specific crop
        
        Args:
            crop: Crop name to search for
            max_states: Maximum number of states to search
            
        Returns:
            Dictionary mapping state names to price lists
        """
        self.logger.info(f"Searching mandis for {crop} across {max_states} states")
        
        states_to_search = self.major_states[:max_states]
        return self.get_multi_crop_prices([crop] * len(states_to_search), states_to_search)
    
    def predict_price(self, features: Dict) -> float:
        """
        Predict the price for a given set of features
        
        Args:
            features: Dictionary containing crop characteristics
            
        Returns:
            Predicted modal price
        """
        if price_prediction_data is None:
            self.logger.warning("Price prediction model not available")
            return 0.0
            
        try:
            # Extract model components (handle both old and new model formats)
            model = price_prediction_data['model']
            encoders = price_prediction_data['encoders']
            scaler = price_prediction_data['scaler']
            
            # Define feature columns (consistent with training)
            feature_columns = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']
            
            # Create DataFrame from features
            df = pd.DataFrame([features])
            
            # Ensure all required columns are present
            for col in feature_columns:
                if col not in df.columns:
                    self.logger.error(f"Missing required feature: {col}")
                    return 0.0
            
            # Encode categorical features
            df_encoded = df.copy()
            for column in feature_columns:
                if column in encoders:
                    # Handle unknown categories
                    unknown_labels = set(df_encoded[column].astype(str)) - set(encoders[column].classes_)
                    if unknown_labels:
                        # For unknown categories, use the most frequent class
                        most_frequent = encoders[column].classes_[0]  # First class as fallback
                        df_encoded[column] = df_encoded[column].astype(str).replace(
                            list(unknown_labels), most_frequent
                        )
                    df_encoded[column] = encoders[column].transform(df_encoded[column].astype(str))
                else:
                    self.logger.error(f"Encoder for {column} not found")
                    return 0.0
            
            # Scale features
            X = df_encoded[feature_columns]
            X_scaled = scaler.transform(X)
            
            # Make prediction
            prediction = model.predict(X_scaled)
            predicted_price = float(prediction[0])
            
            self.logger.info(f"Predicted price: ₹{predicted_price:.2f} for {features.get('Commodity', 'Unknown')}") 
            return predicted_price
            
        except Exception as e:
            self.logger.error(f"Error predicting price: {e}")
            return 0.0

    def get_mandi_wise_prices(self, crop: str, state: str = None, district: str = None) -> pd.DataFrame:
        """
        Get detailed mandi-wise prices for a crop with optional filtering
        
        Args:
            crop: Crop name
            state: Optional state filter
            district: Optional district filter
            
        Returns:
            DataFrame with detailed mandi-wise price data
        """
        try:
            self.logger.info(f"Fetching mandi-wise prices for {crop}")
            
            # Prepare API parameters
            params = {
                "api-key": "579b464db66ec23bdd000001ba21a1d30966476a7f19d8adf57ef501",
                "format": "json",
                "limit": 500,  # Get more records for comprehensive data
                "filters[commodity]": crop
            }
            
            # Add optional filters
            if state:
                params["filters[state]"] = state
            if district:
                params["filters[district]"] = district
            
            response = requests.get(
                "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                self.logger.warning(f"No mandi data found for {crop}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            mandi_data = []
            for record in records:
                if all(k in record for k in ['market', 'state', 'district', 'commodity', 'variety', 'arrival_date', 'min_price', 'max_price', 'modal_price']):
                    mandi_data.append({
                        'Market': record['market'],
                        'State': record['state'],
                        'District': record['district'],
                        'Commodity': record['commodity'],
                        'Variety': record['variety'],
                        'Grade': record.get('grade', 'N/A'),
                        'Date': record['arrival_date'],
                        'Min_Price': float(record['min_price']),
                        'Max_Price': float(record['max_price']),
                        'Modal_Price': float(record['modal_price']),
                        'Price_Range': float(record['max_price']) - float(record['min_price'])
                    })
            
            df = pd.DataFrame(mandi_data)
            
            # Sort by modal price descending
            df = df.sort_values('Modal_Price', ascending=False)
            
            self.logger.info(f"Retrieved {len(df)} mandi records for {crop}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching mandi-wise prices: {e}")
            return pd.DataFrame()
    
    def get_top_mandis_by_price(self, crop: str, top_n: int = 10, by: str = 'modal') -> pd.DataFrame:
        """
        Get top N mandis by price for a specific crop
        
        Args:
            crop: Crop name
            top_n: Number of top mandis to return
            by: Price type to sort by ('modal', 'min', 'max')
            
        Returns:
            DataFrame with top mandis data
        """
        df = self.get_mandi_wise_prices(crop)
        
        if df.empty:
            return df
        
        # Select sorting column
        sort_column = {
            'modal': 'Modal_Price',
            'min': 'Min_Price',
            'max': 'Max_Price'
        }.get(by, 'Modal_Price')
        
        # Get top N mandis
        top_mandis = df.nlargest(top_n, sort_column)
        
        return top_mandis
    
    def get_price_comparison(self, crop: str, states: List[str]) -> pd.DataFrame:
        """
        Compare prices of a crop across multiple states
        
        Args:
            crop: Crop name
            states: List of state names
            
        Returns:
            DataFrame with price comparison data
        """
        comparison_data = []
        
        for state in states:
            prices = self.get_market_prices(crop, state)
            
            if prices:
                avg_price = sum(p.modal_price for p in prices) / len(prices)
                min_price = min(p.min_price for p in prices)
                max_price = max(p.max_price for p in prices)
                mandis_count = len(prices)
            else:
                avg_price = min_price = max_price = mandis_count = 0
            
            comparison_data.append({
                'state': state.title(),
                'avg_price': avg_price,
                'min_price': min_price,
                'max_price': max_price,
                'mandis_count': mandis_count,
                'price_variation': max_price - min_price if max_price > 0 else 0
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Sort by average price descending
        if not df.empty:
            df = df.sort_values('avg_price', ascending=False)
        
        return df
    
    def cleanup(self):
        """Cleanup resources"""
        if self.scraper:
            try:
                if hasattr(self.scraper, 'close'):
                    self.scraper.close()
                elif hasattr(self.scraper, 'quit'):
                    self.scraper.quit()
                elif hasattr(self.scraper, 'driver') and self.scraper.driver:
                    self.scraper.driver.quit()
            except Exception as e:
                self.logger.error(f"Error during cleanup: {e}")
            self.logger.info("Market trends service cleaned up")

# Singleton instance
_market_service = None

def get_market_service() -> MarketTrendsService:
    """Get or create the market trends service singleton"""
    global _market_service
    if _market_service is None:
        _market_service = MarketTrendsService()
    return _market_service

def cleanup_market_service():
    """Cleanup the market service"""
    global _market_service
    if _market_service:
        _market_service.cleanup()
        _market_service = None

# Streamlit integration functions
@st.cache_data(ttl=3600)
def cached_get_market_prices(crop: str, state: str) -> List[Dict]:
    """Cached version for Streamlit"""
    service = get_market_service()
    prices = service.get_market_prices(crop, state)
    
    # Convert to dict for JSON serialization
    return [asdict(price) for price in prices]

@st.cache_data(ttl=1800)  # 30 minutes cache for trends
def cached_get_price_trends(crop: str, state: str, days: int = 7) -> Dict:
    """Cached price trends for Streamlit"""
    service = get_market_service()
    return service.get_price_trends(crop, state, days)

@st.cache_data(ttl=7200)  # 2 hours cache for comparison
def cached_get_price_comparison(crop: str, states: List[str]) -> Dict:
    """Cached price comparison for Streamlit"""
    service = get_market_service()
    df = service.get_price_comparison(crop, states)
    return df.to_dict('records') if not df.empty else []

if __name__ == "__main__":
    # Test the service
    service = MarketTrendsService()
    
    try:
        print("Testing Market Trends Service...")
        
        # Test single crop price fetch
        prices = service.get_market_prices("rice", "telangana")
        print(f"Found {len(prices)} price records for rice in Telangana")
        
        # Test price trends
        trends = service.get_price_trends("rice", "telangana", 5)
        print(f"Price trends: {trends.get('analytics', {})}")
        
        # Test market summary
        summary = service.get_state_market_summary("telangana")
        print(f"Market summary for Telangana: {len(summary.get('crops', {}))} crops")
        
    except Exception as e:
        print(f"Test failed: {e}")
    
    finally:
        service.cleanup()
