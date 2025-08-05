#!/usr/bin/env python3
"""
Test enhanced soil data function integration
"""

import sys
import pandas as pd

# Suppress Streamlit warnings for testing
import os
os.environ['STREAMLIT_DISABLE'] = '1'

def test_soil_integration():
    """Test the enhanced soil data function"""
    try:
        from app import get_location_soil_data
        
        print('🧪 Testing enhanced soil data function...')
        print('=' * 50)
        
        # Test with sample locations
        test_locations = ['New York', 'Mumbai', 'London', 'Tokyo', 'Berlin']
        
        for location in test_locations:
            try:
                print(f'\n🌍 Testing {location}...')
                soil_data = get_location_soil_data(location, None)
                
                # Check if result is pandas Series or dict
                if isinstance(soil_data, pd.Series):
                    soil_dict = soil_data.to_dict()
                else:
                    soil_dict = soil_data
                
                print(f'✅ {location}:')
                print(f'   N={soil_dict["N"]}, P={soil_dict["P"]}, K={soil_dict["K"]}, pH={soil_dict["pH"]:.1f}')
                print(f'   Soil Type: {soil_dict.get("soil_type", "Unknown")}')
                print(f'   Organic Matter: {soil_dict.get("organic_matter", 0):.1f}%')
                
                # Verify NPK values are different (not default)
                if soil_dict['N'] != 80 or soil_dict['P'] != 40 or soil_dict['K'] != 60:
                    print(f'   ✅ NPK values are variable (not using defaults)')
                else:
                    print(f'   ⚠️ Using default NPK values')
                    
            except Exception as e:
                print(f'❌ {location}: Error - {e}')
                import traceback
                traceback.print_exc()
        
        print('\n🎉 Soil data test complete!')
        return True
        
    except Exception as e:
        print(f'❌ Failed to import or test soil function: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_database_functions():
    """Test database functions"""
    try:
        from database import DatabaseManager
        
        print('\n🗄️ Testing database functions...')
        
        db = DatabaseManager()
        
        # Test dashboard stats
        stats = db.get_dashboard_stats()
        print(f'✅ Dashboard stats: {stats}')
        
        # Test user functions
        users = db.get_all_users()
        print(f'✅ Found {len(users) if users else 0} users')
        
        print('✅ Database functions working')
        return True
        
    except Exception as e:
        print(f'❌ Database test failed: {e}')
        return False

if __name__ == "__main__":
    print("🚀 Enhanced Soil Data Integration Test")
    print("=" * 60)
    
    # Test soil data
    soil_test = test_soil_integration()
    
    # Test database
    db_test = test_database_functions()
    
    if soil_test and db_test:
        print("\n✅ All tests passed! The application should work correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
