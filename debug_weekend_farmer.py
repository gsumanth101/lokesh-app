#!/usr/bin/env python3
import sqlite3
import hashlib
from database import DatabaseManager

def debug_weekend_farmer_creation():
    """Debug weekend farmer creation issue"""
    print("=== DEBUG: Weekend Farmer Creation ===")
    
    # Initialize database manager manually
    db_manager = DatabaseManager()
    
    # Test get_user_by_email for weekend farmer
    weekend_farmer_email = "weekendfarmer@smartfarm.com"
    existing_user = db_manager.get_user_by_email(weekend_farmer_email)
    
    print(f"Existing user check for {weekend_farmer_email}: {existing_user}")
    
    if not existing_user:
        print("User does not exist, attempting to create...")
        
        # Try to create weekend farmer manually
        user_id = db_manager.create_user(
            name="Weekend Farmer",
            email=weekend_farmer_email,
            password="weekend123",
            role="weekend_farmer",
            phone="7777777777",
            address="Farm Location",
            location="Weekend Farm Area"
        )
        
        print(f"User creation result: {user_id}")
        
        if user_id:
            print("✅ Weekend farmer created successfully!")
            
            # Verify creation
            created_user = db_manager.get_user_by_email(weekend_farmer_email)
            print(f"Verification: {created_user}")
            
            # Test authentication
            auth_result = db_manager.authenticate_user(weekend_farmer_email, "weekend123")
            print(f"Authentication test: {auth_result}")
        else:
            print("❌ Failed to create weekend farmer")
            
            # Check database constraints
            conn = sqlite3.connect("smart_farming.db")
            cursor = conn.cursor()
            
            # Check table structure
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            print("Users table structure:")
            for col in columns:
                print(f"  {col}")
            
            # Check constraints
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
            table_sql = cursor.fetchone()[0]
            print(f"Table creation SQL: {table_sql}")
            
            conn.close()
    else:
        print("User already exists!")
        
        # Test authentication
        auth_result = db_manager.authenticate_user(weekend_farmer_email, "weekend123")
        print(f"Authentication test: {auth_result}")

if __name__ == "__main__":
    debug_weekend_farmer_creation()
