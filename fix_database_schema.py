#!/usr/bin/env python3
import sqlite3
import os

def fix_database_schema():
    """Fix database schema to include weekend_farmer role"""
    print("=== FIXING DATABASE SCHEMA ===")
    
    # Backup the current database
    if os.path.exists("smart_farming.db"):
        print("Backing up current database...")
        os.system("copy smart_farming.db smart_farming_backup.db")
    
    conn = sqlite3.connect("smart_farming.db")
    cursor = conn.cursor()
    
    # First, let's see what we have
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
    current_sql = cursor.fetchone()[0]
    print(f"Current users table SQL: {current_sql}")
    
    # Check if weekend_farmer is in the constraint
    if 'weekend_farmer' not in current_sql:
        print("❌ weekend_farmer not in role constraint. Fixing...")
        
        # We need to recreate the table with the correct constraint
        # Step 1: Create a new table with the correct constraint
        cursor.execute('''
            CREATE TABLE users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin', 'farmer', 'buyer', 'agent', 'weekend_farmer')),
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                location TEXT
            )
        ''')
        
        # Step 2: Copy all data from old table to new table
        cursor.execute('''
            INSERT INTO users_new 
            SELECT id, name, email, password_hash, role, phone, address, created_at, is_active, location
            FROM users
        ''')
        
        # Step 3: Drop old table
        cursor.execute('DROP TABLE users')
        
        # Step 4: Rename new table
        cursor.execute('ALTER TABLE users_new RENAME TO users')
        
        conn.commit()
        print("✅ Database schema fixed!")
        
        # Verify the fix
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
        new_sql = cursor.fetchone()[0]
        print(f"New users table SQL: {new_sql}")
        
    else:
        print("✅ weekend_farmer already in role constraint")
    
    conn.close()
    
    # Now recreate the weekend farmer
    print("\n=== CREATING WEEKEND FARMER ===")
    from database import DatabaseManager
    
    db_manager = DatabaseManager()
    
    # Check if weekend farmer exists
    weekend_farmer_email = "weekendfarmer@smartfarm.com"
    existing_user = db_manager.get_user_by_email(weekend_farmer_email)
    
    if not existing_user:
        # Create weekend farmer
        user_id = db_manager.create_user(
            name="Weekend Farmer",
            email=weekend_farmer_email,
            password="weekend123",
            role="weekend_farmer",
            phone="7777777777",
            address="Farm Location",
            location="Weekend Farm Area"
        )
        
        if user_id:
            print(f"✅ Weekend farmer created with ID: {user_id}")
            
            # Test authentication
            auth_result = db_manager.authenticate_user(weekend_farmer_email, "weekend123")
            print(f"✅ Authentication test: {auth_result}")
        else:
            print("❌ Failed to create weekend farmer")
    else:
        print(f"✅ Weekend farmer already exists: {existing_user}")
    
    print("\n=== SCHEMA FIX COMPLETE ===")

if __name__ == "__main__":
    fix_database_schema()
