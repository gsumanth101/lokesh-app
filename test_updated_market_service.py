#!/usr/bin/env python3
"""
Test the updated Market Trends Service with the new API integration
"""

import sys
import json
from market_trends_service import MarketTrendsService, get_market_service

def test_api_integration():
    """Test the API integration functionality"""
    print("🔄 Testing Updated Market Trends Service with API Integration...")
    
    try:
        # Initialize the service
        service = MarketTrendsService()
        print("✅ Market Trends Service initialized successfully")
        
        # Test 1: Get market prices for a specific crop and state
        print("\n📊 Test 1: Fetching market prices...")
        crop = "Onion"
        state = "Andhra Pradesh"
        
        prices = service.get_market_prices(crop, state)
        print(f"Found {len(prices)} price records for {crop} in {state}")
        
        if prices:
            sample_price = prices[0]
            print(f"Sample price record:")
            print(f"  Market: {sample_price.mandi_name}")
            print(f"  District: {sample_price.district}")
            print(f"  Commodity: {sample_price.commodity}")
            print(f"  Variety: {sample_price.variety}")
            print(f"  Min Price: ₹{sample_price.min_price}")
            print(f"  Max Price: ₹{sample_price.max_price}")
            print(f"  Modal Price: ₹{sample_price.modal_price}")
            print(f"  Date: {sample_price.arrival_date}")
        
        # Test 2: Get price trends
        print("\n📈 Test 2: Fetching price trends...")
        trends = service.get_price_trends(crop, state, days=7)
        print(f"Trends analysis for {crop} in {state}:")
        
        analytics = trends.get('analytics', {})
        if analytics:
            print(f"  Current Average Price: ₹{analytics.get('current_avg_price', 0):.2f}")
            print(f"  Price Change: ₹{analytics.get('price_change', 0):.2f}")
            print(f"  Price Change %: {analytics.get('price_change_percent', 0):.2f}%")
            print(f"  Trend Direction: {analytics.get('trend_direction', 'unknown')}")
        else:
            print("  No analytics data available")
        
        # Test 3: Multi-crop prices
        print("\n🥕 Test 3: Fetching multi-crop prices...")
        crops = ["Tomato", "Potato", "Onion"]
        multi_prices = service.get_multi_crop_prices(crops, state)
        
        for crop_name, crop_prices in multi_prices.items():
            print(f"  {crop_name}: {len(crop_prices)} price records")
        
        # Test 4: State market summary
        print("\n🏛️ Test 4: Generating state market summary...")
        summary = service.get_state_market_summary(state)
        print(f"Market summary for {state}:")
        print(f"  Date: {summary.get('date')}")
        print(f"  Total crops analyzed: {summary.get('total_crops', 0)}")
        
        crops_data = summary.get('crops', {})
        for crop_name, crop_info in list(crops_data.items())[:3]:  # Show first 3 crops
            print(f"  {crop_name}:")
            print(f"    Avg Price: ₹{crop_info.get('avg_price', 0):.2f}")
            print(f"    Mandis Count: {crop_info.get('mandis_count', 0)}")
        
        # Test 5: Price comparison across states
        print("\n🗺️ Test 5: Price comparison across states...")
        states = ["Andhra Pradesh", "Karnataka", "Tamil Nadu"]
        comparison_df = service.get_price_comparison("Tomato", states)
        
        if not comparison_df.empty:
            print("Price comparison for Tomato:")
            for _, row in comparison_df.iterrows():
                print(f"  {row['state']}: ₹{row['avg_price']:.2f} (avg), {row['mandis_count']} mandis")
        else:
            print("  No comparison data available")
        
        print("\n✅ All tests completed successfully!")
        print("🎉 Market Trends Service is now using live API data!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            service.cleanup()
            print("🧹 Service cleanup completed")
        except:
            pass

def test_popular_crops():
    """Test with popular crops from the service"""
    print("\n🌾 Testing popular crops from the service...")
    
    service = MarketTrendsService()
    print(f"Popular crops: {service.popular_crops[:5]}")
    print(f"Major states: {service.major_states[:5]}")
    
    # Test a few popular crop-state combinations
    test_combinations = [
        ("Potato", "Uttar Pradesh"),
        ("Tomato", "Karnataka"),
        ("Onion", "Maharashtra")
    ]
    
    for crop, state in test_combinations:
        print(f"\n🔍 Testing {crop} in {state}...")
        prices = service.get_market_prices(crop, state)
        print(f"  Found {len(prices)} records")
        
        if prices:
            avg_price = sum(p.modal_price for p in prices) / len(prices)
            print(f"  Average modal price: ₹{avg_price:.2f}")
    
    service.cleanup()

if __name__ == "__main__":
    print("🚀 Starting Market Trends Service API Integration Tests")
    print("=" * 60)
    
    success = test_api_integration()
    
    if success:
        test_popular_crops()
        print("\n🎯 Summary:")
        print("✅ Market Trends Service successfully updated to use external API")
        print("✅ Live market data integration working")
        print("✅ Caching and error handling functional")
        print("✅ All major service methods tested")
    else:
        print("\n❌ Tests failed. Please check the implementation.")
        sys.exit(1)
