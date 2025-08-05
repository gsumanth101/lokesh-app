#!/usr/bin/env python3
import sqlite3
import hashlib

def check_weekend_farmers():
    """Check weekend farmer users in database"""
    conn = sqlite3.connect("smart_farming.db")
    cursor = conn.cursor()
    
    print("=== Checking Weekend Farmers ===")
    
    # Check all users with weekend_farmer role
    cursor.execute("SELECT id, name, email, role, is_active FROM users WHERE role = 'weekend_farmer'")
    weekend_farmers = cursor.fetchall()
    
    if weekend_farmers:
        print(f"Found {len(weekend_farmers)} weekend farmer(s):")
        for wf in weekend_farmers:
            print(f"  ID: {wf[0]}, Name: {wf[1]}, Email: {wf[2]}, Role: {wf[3]}, Active: {wf[4]}")
    else:
        print("No weekend farmers found!")
    
    # Test authentication for weekend farmer
    email = "weekendfarmer@smartfarm.com"
    password = "weekend123"
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        SELECT id, name, email, role, is_active
        FROM users
        WHERE email = ? AND password_hash = ? AND is_active = 1
    ''', (email, password_hash))
    
    auth_result = cursor.fetchone()
    
    print(f"\n=== Authentication Test ===")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Hash: {password_hash}")
    
    if auth_result:
        print(f"✅ Authentication SUCCESS: {auth_result}")
    else:
        print("❌ Authentication FAILED")
        
        # Check if user exists with different hash
        cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,))
        user_check = cursor.fetchone()
        if user_check:
            print(f"User exists but password hash mismatch:")
            print(f"  Expected: {password_hash}")
            print(f"  Actual:   {user_check[3]}")
        else:
            print("User does not exist at all!")
    
    conn.close()

if __name__ == "__main__":
    check_weekend_farmers()
