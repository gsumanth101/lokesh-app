#!/usr/bin/env python3
"""
Smart Farming Assistant - Dummy Login Credentials Display
This script shows all the available dummy login credentials for testing.
"""

import sqlite3
from database import DatabaseManager

def display_dummy_logins():
    """Display all available dummy login credentials"""
    
    print("=" * 60)
    print("🌾 SMART FARMING ASSISTANT - DUMMY LOGIN CREDENTIALS")
    print("=" * 60)
    print()
    
    # Initialize database manager (this will create default users if they don't exist)
    db_manager = DatabaseManager()
    
    # Get all users from database
    conn = sqlite3.connect("smart_farming.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, email, role, phone, address, location 
        FROM users 
        ORDER BY role, name
    """)
    users = cursor.fetchall()
    conn.close()
    
    # Group users by role
    users_by_role = {}
    for user in users:
        name, email, role, phone, address, location = user
        if role not in users_by_role:
            users_by_role[role] = []
        users_by_role[role].append({
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'location': location
        })
    
    # Display default credentials
    print("📋 DEFAULT DUMMY CREDENTIALS:")
    print("-" * 40)
    
    default_credentials = {
        'admin': {'email': 'admin@smartfarm.com', 'password': 'admin123'},
        'agent': {'email': 'agent@smartfarm.com', 'password': 'agent123'},
        'weekend_farmer': {'email': 'weekendfarmer@smartfarm.com', 'password': 'weekend123'}
    }
    
    for role, creds in default_credentials.items():
        print(f"🔑 {role.upper()} LOGIN:")
        print(f"   Email: {creds['email']}")
        print(f"   Password: {creds['password']}")
        print()
    
    # Display all users in database
    print("👥 ALL USERS IN DATABASE:")
    print("-" * 40)
    
    role_icons = {
        'admin': '🛡️',
        'farmer': '👨‍🌾',
        'buyer': '🛒',
        'agent': '🤝',
        'weekend_farmer': '🌾'
    }
    
    for role, user_list in users_by_role.items():
        icon = role_icons.get(role, '👤')
        print(f"{icon} {role.upper()}S ({len(user_list)}):")
        for user in user_list:
            print(f"   • {user['name']} ({user['email']})")
            if user['phone']:
                print(f"     Phone: {user['phone']}")
            if user['location']:
                print(f"     Location: {user['location']}")
        print()
    
    print("=" * 60)
    print("🚀 HOW TO USE:")
    print("1. Run: streamlit run app.py")
    print("2. Use any of the credentials above to login")
    print("3. Each role has different dashboard features")
    print("=" * 60)
    print()

def create_additional_dummy_users():
    """Create additional dummy users for testing"""
    
    db_manager = DatabaseManager()
    
    # Additional dummy users
    additional_users = [
        {
            'name': 'John Farmer',
            'email': 'john.farmer@test.com',
            'password': 'Test123!',
            'role': 'farmer',
            'phone': '9876543210',
            'address': 'Village Farm Area',
            'location': 'Punjab, India'
        },
        {
            'name': 'Sarah Buyer',
            'email': 'sarah.buyer@test.com',
            'password': 'Test123!',
            'role': 'buyer',
            'phone': '9876543211',
            'address': 'City Market Area',
            'location': 'Mumbai, India'
        },
        {
            'name': 'Mike Agent',
            'email': 'mike.agent@test.com',
            'password': 'Test123!',
            'role': 'agent',
            'phone': '9876543212',
            'address': 'Agent Office',
            'location': 'Delhi, India'
        },
        {
            'name': 'Emma Weekend',
            'email': 'emma.weekend@test.com',
            'password': 'Test123!',
            'role': 'weekend_farmer',
            'phone': '9876543213',
            'address': 'Suburban Area',
            'location': 'Bangalore, India'
        }
    ]
    
    print("🔧 CREATING ADDITIONAL DUMMY USERS...")
    print("-" * 40)
    
    for user_data in additional_users:
        user_id = db_manager.create_user(
            name=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role'],
            phone=user_data['phone'],
            address=user_data['address'],
            location=user_data['location']
        )
        
        if user_id:
            print(f"✅ Created: {user_data['name']} ({user_data['email']})")
        else:
            print(f"⚠️  Already exists: {user_data['name']} ({user_data['email']})")
    
    print()

if __name__ == "__main__":
    # Create additional dummy users first
    create_additional_dummy_users()
    
    # Display all login credentials
    display_dummy_logins()
