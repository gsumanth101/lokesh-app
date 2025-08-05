#!/usr/bin/env python3
"""
Comprehensive Mandi-Wise Price Display Script
Shows detailed mandi information with user-friendly formatting
"""

import pandas as pd
from market_trends_service import MarketTrendsService

def display_mandi_prices(crop: str, state: str = None, district: str = None, top_n: int = 20):
    """
    Display detailed mandi-wise prices for a crop
    
    Args:
        crop: Crop name
        state: Optional state filter
        district: Optional district filter
        top_n: Number of top mandis to display
    """
    service = MarketTrendsService()
    
    try:
        print(f"🌾 MANDI-WISE PRICES FOR {crop.upper()}")
        if state:
            print(f"📍 State: {state}")
        if district:
            print(f"🏘️ District: {district}")
        print("=" * 80)
        
        # Get mandi-wise prices
        df = service.get_mandi_wise_prices(crop, state, district)
        
        if df.empty:
            print("❌ No mandi data found for the specified criteria.")
            return
        
        # Display summary statistics
        print(f"📊 SUMMARY:")
        print(f"   Total Mandis: {len(df)}")
        print(f"   Average Modal Price: ₹{df['Modal_Price'].mean():.2f}")
        print(f"   Highest Price: ₹{df['Modal_Price'].max():.2f}")
        print(f"   Lowest Price: ₹{df['Modal_Price'].min():.2f}")
        print(f"   Price Range: ₹{df['Modal_Price'].max() - df['Modal_Price'].min():.2f}")
        print()
        
        # Display top mandis
        print(f"🏆 TOP {min(top_n, len(df))} MANDIS BY MODAL PRICE:")
        print("-" * 80)
        
        # Set pandas display options for better formatting
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 20)
        
        # Display detailed mandi information
        for idx, (_, row) in enumerate(df.head(top_n).iterrows(), 1):
            print(f"{idx:2d}. {row['Market']} ({row['District']}, {row['State']})")
            print(f"    Variety: {row['Variety']} | Grade: {row['Grade']} | Date: {row['Date']}")
            print(f"    Min: ₹{row['Min_Price']:.0f} | Max: ₹{row['Max_Price']:.0f} | Modal: ₹{row['Modal_Price']:.0f}")
            print(f"    Price Range: ₹{row['Price_Range']:.0f}")
            print()
        
        # Display state-wise summary if no state filter is applied
        if not state and len(df) > 1:
            print("🗺️ STATE-WISE SUMMARY:")
            print("-" * 40)
            state_summary = df.groupby('State').agg({
                'Modal_Price': ['mean', 'min', 'max', 'count']
            }).round(2)
            state_summary.columns = ['Avg_Price', 'Min_Price', 'Max_Price', 'Mandi_Count']
            state_summary = state_summary.sort_values('Avg_Price', ascending=False)
            
            for state_name, row in state_summary.iterrows():
                print(f"  {state_name}:")
                print(f"    Avg: ₹{row['Avg_Price']:.2f} | Min: ₹{row['Min_Price']:.0f} | Max: ₹{row['Max_Price']:.0f} | Mandis: {int(row['Mandi_Count'])}")
        
        # Display district-wise summary if state is specified but not district
        if state and not district and len(df) > 1:
            print(f"🏘️ DISTRICT-WISE SUMMARY FOR {state.upper()}:")
            print("-" * 50)
            district_summary = df.groupby('District').agg({
                'Modal_Price': ['mean', 'min', 'max', 'count']
            }).round(2)
            district_summary.columns = ['Avg_Price', 'Min_Price', 'Max_Price', 'Mandi_Count']
            district_summary = district_summary.sort_values('Avg_Price', ascending=False)
            
            for district_name, row in district_summary.iterrows():
                print(f"  {district_name}:")
                print(f"    Avg: ₹{row['Avg_Price']:.2f} | Min: ₹{row['Min_Price']:.0f} | Max: ₹{row['Max_Price']:.0f} | Mandis: {int(row['Mandi_Count'])}")
        
    except Exception as e:
        print(f"❌ Error fetching mandi prices: {e}")
    
    finally:
        service.cleanup()

def display_comparative_mandi_analysis(crops: list, state: str = None):
    """
    Display comparative mandi analysis for multiple crops
    
    Args:
        crops: List of crop names
        state: Optional state filter
    """
    service = MarketTrendsService()
    
    try:
        print(f"🔄 COMPARATIVE MANDI ANALYSIS")
        if state:
            print(f"📍 State: {state}")
        print("=" * 80)
        
        comparative_data = []
        
        for crop in crops:
            df = service.get_mandi_wise_prices(crop, state)
            if not df.empty:
                comparative_data.append({
                    'Crop': crop,
                    'Mandis_Count': len(df),
                    'Avg_Price': df['Modal_Price'].mean(),
                    'Min_Price': df['Modal_Price'].min(),
                    'Max_Price': df['Modal_Price'].max(),
                    'Price_Variation': df['Modal_Price'].std()
                })
        
        if comparative_data:
            comp_df = pd.DataFrame(comparative_data)
            comp_df = comp_df.sort_values('Avg_Price', ascending=False)
            
            print("📊 CROP COMPARISON:")
            print("-" * 80)
            
            for _, row in comp_df.iterrows():
                print(f"{row['Crop']:15} | Mandis: {int(row['Mandis_Count']):3d} | "
                      f"Avg: ₹{row['Avg_Price']:7.2f} | Min: ₹{row['Min_Price']:7.0f} | "
                      f"Max: ₹{row['Max_Price']:7.0f} | Variation: ₹{row['Price_Variation']:6.2f}")
        else:
            print("❌ No data found for the specified crops.")
    
    except Exception as e:
        print(f"❌ Error in comparative analysis: {e}")
    
    finally:
        service.cleanup()

def main():
    """Main function to demonstrate mandi-wise price functionality"""
    print("🚀 MANDI-WISE PRICE ANALYSIS SYSTEM")
    print("=" * 80)
    
    # Example 1: Onion prices in Andhra Pradesh
    print("\n📍 EXAMPLE 1: Onion prices in Andhra Pradesh")
    display_mandi_prices("Onion", state="Andhra Pradesh", top_n=10)
    
    print("\n" + "="*80 + "\n")
    
    # Example 2: Tomato prices across all states (top 15)
    print("📍 EXAMPLE 2: Tomato prices across all states")
    display_mandi_prices("Tomato", top_n=15)
    
    print("\n" + "="*80 + "\n")
    
    # Example 3: Comparative analysis
    print("📍 EXAMPLE 3: Comparative analysis of popular crops")
    display_comparative_mandi_analysis(["Onion", "Tomato", "Potato"], state="Karnataka")

if __name__ == "__main__":
    main()
