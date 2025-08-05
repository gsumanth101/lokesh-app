import pandas as pd
from database import DatabaseManager
from datetime import datetime
import os

# Define comprehensive crop data with realistic Indian market prices (per quintal)
all_crops = [
    # Fruits
    {'Crop': 'apple', 'Price': 8000, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'banana', 'Price': 2500, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'grapes', 'Price': 6000, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'mango', 'Price': 4500, 'Unit': 'quintal', 'Trend': 'Decreasing'},
    {'Crop': 'orange', 'Price': 3500, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'papaya', 'Price': 1800, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'pomegranate', 'Price': 7500, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'watermelon', 'Price': 1200, 'Unit': 'quintal', 'Trend': 'Volatile'},
    {'Crop': 'muskmelon', 'Price': 1500, 'Unit': 'quintal', 'Trend': 'Stable'},
    
    # Cereals & Grains
    {'Crop': 'wheat', 'Price': 2200, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'rice', 'Price': 2800, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'maize', 'Price': 1900, 'Unit': 'quintal', 'Trend': 'Decreasing'},
    {'Crop': 'barley', 'Price': 2100, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'millet', 'Price': 3200, 'Unit': 'quintal', 'Trend': 'Increasing'},
    
    # Pulses & Legumes
    {'Crop': 'blackgram', 'Price': 6500, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'chickpea', 'Price': 5500, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'kidneybeans', 'Price': 8000, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'lentil', 'Price': 7500, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'mothbeans', 'Price': 4500, 'Unit': 'quintal', 'Trend': 'Decreasing'},
    {'Crop': 'mungbean', 'Price': 7800, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'pigeonpeas', 'Price': 6800, 'Unit': 'quintal', 'Trend': 'Stable'},
    
    # Vegetables
    {'Crop': 'tomato', 'Price': 2500, 'Unit': 'quintal', 'Trend': 'Volatile'},
    {'Crop': 'potato', 'Price': 1200, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'onion', 'Price': 1800, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'cabbage', 'Price': 1500, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'cauliflower', 'Price': 2000, 'Unit': 'quintal', 'Trend': 'Decreasing'},
    {'Crop': 'brinjal', 'Price': 2200, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'okra', 'Price': 2800, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'carrot', 'Price': 1800, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'beetroot', 'Price': 2000, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'radish', 'Price': 1200, 'Unit': 'quintal', 'Trend': 'Stable'},
    
    # Cash Crops
    {'Crop': 'cotton', 'Price': 5800, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'sugarcane', 'Price': 300, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'jute', 'Price': 4200, 'Unit': 'quintal', 'Trend': 'Decreasing'},
    {'Crop': 'coconut', 'Price': 12000, 'Unit': 'thousand nuts', 'Trend': 'Stable'},
    {'Crop': 'coffee', 'Price': 15000, 'Unit': 'quintal', 'Trend': 'Increasing'},
    
    # Spices & Others
    {'Crop': 'turmeric', 'Price': 8500, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'chili', 'Price': 12000, 'Unit': 'quintal', 'Trend': 'Volatile'},
    {'Crop': 'coriander', 'Price': 9500, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'cumin', 'Price': 25000, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'fenugreek', 'Price': 6500, 'Unit': 'quintal', 'Trend': 'Decreasing'},
    {'Crop': 'mustard', 'Price': 5200, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'sesame', 'Price': 11000, 'Unit': 'quintal', 'Trend': 'Increasing'},
    {'Crop': 'groundnut', 'Price': 5500, 'Unit': 'quintal', 'Trend': 'Stable'},
    {'Crop': 'sunflower', 'Price': 4800, 'Unit': 'quintal', 'Trend': 'Decreasing'},
    {'Crop': 'soybean', 'Price': 4200, 'Unit': 'quintal', 'Trend': 'Stable'},
]

def update_market_prices_db(crops):
    """Update database with market prices"""
    try:
        db_manager = DatabaseManager()
        success_count = 0
        for crop in crops:
            success = db_manager.update_market_price(
                crop_name=crop['Crop'],
                price=crop['Price'],
                trend=crop['Trend'],
                updated_by_user={'id': 1, 'name': 'System Admin', 'role': 'admin'},
                reason='Comprehensive marketplace update with all crops'
            )
            if success:
                success_count += 1
        print(f"Database updated: {success_count}/{len(crops)} crops")
    except Exception as e:
        print(f"Database update error: {e}")

def create_comprehensive_marketplace():
    """Create comprehensive marketplace CSV file"""
    try:
        # Create DataFrame with all crops
        df_new = pd.DataFrame(all_crops)
        df_new['Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save to CSV
        csv_path = 'data/market_prices.csv'
        if os.path.exists(csv_path):
            # Backup existing file
            backup_path = f'data/market_prices_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            os.rename(csv_path, backup_path)
            print(f"Backup created: {backup_path}")
        
        # Save new comprehensive data
        df_new.to_csv(csv_path, index=False)
        print(f"✅ Market prices updated with {len(all_crops)} crops")
        print(f"📁 File saved: {csv_path}")
        
        # Display summary
        print("\n📊 Crop Categories Added:")
        categories = {
            'Fruits': ['apple', 'banana', 'grapes', 'mango', 'orange', 'papaya', 'pomegranate', 'watermelon', 'muskmelon'],
            'Cereals & Grains': ['wheat', 'rice', 'maize', 'barley', 'millet'],
            'Pulses & Legumes': ['blackgram', 'chickpea', 'kidneybeans', 'lentil', 'mothbeans', 'mungbean', 'pigeonpeas'],
            'Vegetables': ['tomato', 'potato', 'onion', 'cabbage', 'cauliflower', 'brinjal', 'okra', 'carrot', 'beetroot', 'radish'],
            'Cash Crops': ['cotton', 'sugarcane', 'jute', 'coconut', 'coffee'],
            'Spices & Others': ['turmeric', 'chili', 'coriander', 'cumin', 'fenugreek', 'mustard', 'sesame', 'groundnut', 'sunflower', 'soybean']
        }
        
        for category, crops in categories.items():
            print(f"  • {category}: {len(crops)} items")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating marketplace: {e}")
        return False

def display_price_summary():
    """Display price range summary"""
    df = pd.DataFrame(all_crops)
    print("\n💰 Price Range Summary:")
    print(f"   • Lowest Price: ₹{df['Price'].min():,}/quintal ({df.loc[df['Price'].idxmin(), 'Crop']})")
    print(f"   • Highest Price: ₹{df['Price'].max():,}/quintal ({df.loc[df['Price'].idxmax(), 'Crop']})")
    print(f"   • Average Price: ₹{df['Price'].mean():.0f}/quintal")
    
    trend_counts = df['Trend'].value_counts()
    print("\n📈 Market Trends:")
    for trend, count in trend_counts.items():
        print(f"   • {trend}: {count} crops")

if __name__ == "__main__":
    print("🌾 Smart Farming Marketplace Update")
    print("=" * 40)
    
    # Create comprehensive marketplace
    if create_comprehensive_marketplace():
        # Update database
        update_market_prices_db(all_crops)
        
        # Display summary
        display_price_summary()
        
        print("\n✅ Marketplace update completed successfully!")
        print("\n🚀 You can now:")
        print("   • View all crops in the market dashboard")
        print("   • Modify prices through admin/agent interface")
        print("   • Add new crop listings with current market rates")
        print("   • Get AI recommendations for all available crops")
    else:
        print("❌ Marketplace update failed!")
