#!/usr/bin/env python3
"""
Test script for Market Trends Service with Prediction
"""

from market_trends_service import get_market_service
import pandas as pd

def test_market_trends_with_prediction():
    """Test the market trends service with prediction functionality"""
    
    print("=== Market Trends Service Test ===\n")
    
    # Get the service
    service = get_market_service()
    
    try:
        # Test 1: Get market prices
        print("1. Testing market price fetching...")
        prices = service.get_market_prices("rice", "telangana")
        print(f"   ✓ Found {len(prices)} price records for rice in Telangana")
        
        if prices:
            sample_price = prices[0]
            print(f"   Sample price: {sample_price.commodity} - ₹{sample_price.modal_price}/quintal")
        
        # Test 2: Get price trends
        print("\n2. Testing price trends...")
        trends = service.get_price_trends("rice", "telangana", 5)
        if 'analytics' in trends:
            analytics = trends['analytics']
            print(f"   ✓ Current avg price: ₹{analytics.get('current_avg_price', 0):.2f}")
            print(f"   ✓ Price change: ₹{analytics.get('price_change', 0):.2f}")
            print(f"   ✓ Trend direction: {analytics.get('trend_direction', 'unknown')}")
        
        # Test 3: Test price prediction
        print("\n3. Testing price prediction...")
        features = {
            'State': 'Telangana',
            'District': 'Warangal',
            'Market': 'Warangal',
            'Commodity': 'Rice',
            'Variety': 'Common',
            'Grade': 'FAQ'
        }
        
        predicted_price = service.predict_price(features)
        print(f"   ✓ Predicted price for rice in Warangal: ₹{predicted_price:.2f}/quintal")
        
        # Test 4: Multi-crop comparison
        print("\n4. Testing multi-crop price comparison...")
        crops = ['rice', 'wheat', 'maize']
        multi_prices = service.get_multi_crop_prices(crops, 'telangana')
        
        for crop, crop_prices in multi_prices.items():
            if crop_prices:
                avg_price = sum(p.modal_price for p in crop_prices) / len(crop_prices)
                print(f"   ✓ {crop.title()}: ₹{avg_price:.2f}/quintal ({len(crop_prices)} markets)")
            else:
                print(f"   ✗ {crop.title()}: No data available")
        
        # Test 5: State comparison
        print("\n5. Testing state-wise price comparison...")
        states = ['telangana', 'andhra pradesh', 'karnataka']
        comparison_df = service.get_price_comparison('rice', states)
        
        if not comparison_df.empty:
            print("   State-wise Rice Price Comparison:")
            for _, row in comparison_df.iterrows():
                print(f"   ✓ {row['state']}: ₹{row['avg_price']:.2f} (Range: ₹{row['min_price']:.2f} - ₹{row['max_price']:.2f})")
        
        # Test 6: Market summary
        print("\n6. Testing market summary...")
        summary = service.get_state_market_summary('telangana')
        print(f"   ✓ Market summary for Telangana ({summary['total_crops']} crops):")
        
        for crop, data in summary['crops'].items():
            print(f"   - {crop.title()}: ₹{data['avg_price']:.2f} ({data['mandis_count']} mandis)")
        
        print("\n=== All Tests Completed Successfully! ===")
        
    except Exception as e:
        print(f"   ✗ Error during testing: {e}")
        
    finally:
        # Cleanup
        service.cleanup()
        print("\n✓ Service cleaned up successfully")

def test_prediction_with_csv_data():
    """Test prediction using data from the CSV file"""
    
    print("\n=== Testing Prediction with CSV Data ===\n")
    
    try:
        # Load some sample data from the CSV
        csv_path = 'data/markettrends.csv'
        df = pd.read_csv(csv_path)
        
        print(f"Loaded {len(df)} records from CSV")
        
        # Get the service and test prediction on some samples
        service = get_market_service()
        
        # Test prediction on first 5 records
        print("\nTesting predictions on sample data:")
        
        for i in range(min(5, len(df))):
            row = df.iloc[i]
            
            features = {
                'State': row['State'],
                'District': row['District'], 
                'Market': row['Market'],
                'Commodity': row['Commodity'],
                'Variety': row['Variety'],
                'Grade': row['Grade']
            }
            
            actual_price = row['Modal_x0020_Price']
            predicted_price = service.predict_price(features)
            
            print(f"{i+1}. {row['Commodity']} in {row['State']}")
            print(f"   Actual: ₹{actual_price}")
            print(f"   Predicted: ₹{predicted_price:.2f}")
            print(f"   Difference: ₹{abs(actual_price - predicted_price):.2f}")
            print()
        
        service.cleanup()
        
    except Exception as e:
        print(f"Error testing with CSV data: {e}")

if __name__ == "__main__":
    test_market_trends_with_prediction()
    test_prediction_with_csv_data()
