#!/usr/bin/env python3
"""
Analyze the complete markettrends dataset
"""

import pandas as pd

def analyze_dataset():
    """Analyze the markettrends dataset"""
    
    print("=== Market Trends Dataset Analysis ===\n")
    
    # Load the dataset
    df = pd.read_csv('data/markettrends.csv')
    
    print("📊 Dataset Overview:")
    print(f"   Total records: {len(df):,}")
    print(f"   Unique States: {len(df['State'].unique())}")
    print(f"   Unique Districts: {len(df['District'].unique())}")
    print(f"   Unique Markets: {len(df['Market'].unique())}")
    print(f"   Unique Commodities: {len(df['Commodity'].unique())}")
    print(f"   Unique Varieties: {len(df['Variety'].unique())}")
    print(f"   Unique Grades: {len(df['Grade'].unique())}")
    
    print(f"\n🌾 Top 20 Most Common Commodities:")
    commodity_counts = df['Commodity'].value_counts()
    for i, (commodity, count) in enumerate(commodity_counts.head(20).items(), 1):
        print(f"   {i:2d}. {commodity:<25} ({count:3d} records)")
    
    print(f"\n🏛️ Top 10 States by Records:")
    state_counts = df['State'].value_counts()
    for i, (state, count) in enumerate(state_counts.head(10).items(), 1):
        print(f"   {i:2d}. {state:<20} ({count:4d} records)")
    
    print(f"\n💰 Price Range Analysis:")
    print(f"   Minimum Price: ₹{df['Modal_x0020_Price'].min():,.2f}")
    print(f"   Maximum Price: ₹{df['Modal_x0020_Price'].max():,.2f}")
    print(f"   Average Price: ₹{df['Modal_x0020_Price'].mean():,.2f}")
    print(f"   Median Price:  ₹{df['Modal_x0020_Price'].median():,.2f}")
    
    print(f"\n🎯 High-Value Commodities (Top 10 by Average Price):")
    avg_prices = df.groupby('Commodity')['Modal_x0020_Price'].agg(['mean', 'count']).reset_index()
    avg_prices = avg_prices[avg_prices['count'] >= 3]  # Only commodities with at least 3 records
    avg_prices = avg_prices.sort_values('mean', ascending=False)
    
    for i, row in avg_prices.head(10).iterrows():
        print(f"   {i+1:2d}. {row['Commodity']:<25} ₹{row['mean']:8,.2f} ({row['count']:2d} records)")
    
    print(f"\n📈 All Commodities List:")
    all_commodities = sorted(df['Commodity'].unique())
    print(f"   Total: {len(all_commodities)} unique commodities")
    
    # Save commodities list to file
    with open('all_commodities.txt', 'w', encoding='utf-8') as f:
        for i, commodity in enumerate(all_commodities, 1):
            f.write(f"{i}. {commodity}\n")
            
    print(f"   ✅ Complete list saved to 'all_commodities.txt'")
    
    return all_commodities, df

if __name__ == "__main__":
    commodities, dataset = analyze_dataset()
