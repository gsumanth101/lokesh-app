#!/usr/bin/env python3
"""
Test script for fetching mandi-wise prices using the Market Trends Service
"""

from market_trends_service import MarketTrendsService

def test_mandi_wise_prices():
    """Test the fetching of mandi-wise prices."""
    service = MarketTrendsService()
    
    # Mandi-wise prices for Onion in Andhra Pradesh
    print("🔍 Fetching mandi-wise prices for Onion in Andhra Pradesh...")
    df_mandi_prices = service.get_mandi_wise_prices(crop="Onion", state="Andhra Pradesh")
    if not df_mandi_prices.empty:
        print(df_mandi_prices.head())
    else:
        print("No mandi-wise price data available.")

    # Top 5 mandis by modal price
    print("\n🌟 Fetching top 5 mandis by modal price for Onion...")
    df_top_mandis = service.get_top_mandis_by_price(crop="Onion", top_n=5, by="modal")
    if not df_top_mandis.empty:
        print(df_top_mandis)
    else:
        print("No top mandi data available.")

    # Cleanup
    service.cleanup()
    print("🧹 Service cleanup completed.")

if __name__ == "__main__":
    print("🚀 Starting Mandi-Wise Price Tests")
    print("=" * 60)
    
    test_mandi_wise_prices()

