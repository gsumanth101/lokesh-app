import sqlite3
import hashlib
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path: str = "smart_farming.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('admin', 'farmer', 'buyer', 'agent', 'weekend_farmer')),
                phone TEXT,
                address TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Crop listings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crop_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER NOT NULL,
                crop_name TEXT NOT NULL,
                quantity REAL NOT NULL,
                expected_price REAL NOT NULL,
                description TEXT,
                location TEXT,
                status TEXT DEFAULT 'available' CHECK (status IN ('available', 'sold', 'cancelled')),
                farmer_name TEXT,
                farmer_phone TEXT,
                agent_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farmer_id) REFERENCES users (id),
                FOREIGN KEY (agent_id) REFERENCES users (id)
            )
        ''')
        
        # Buyer offers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buyer_offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buyer_id INTEGER NOT NULL,
                crop_listing_id INTEGER,
                crop_name TEXT NOT NULL,
                offer_price REAL NOT NULL,
                quantity_wanted REAL NOT NULL,
                notes TEXT,
                status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'cancelled')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (buyer_id) REFERENCES users (id),
                FOREIGN KEY (crop_listing_id) REFERENCES crop_listings (id)
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buyer_id INTEGER NOT NULL,
                farmer_id INTEGER NOT NULL,
                crop_listing_id INTEGER NOT NULL,
                crop_name TEXT NOT NULL,
                quantity REAL NOT NULL,
                price_per_unit REAL NOT NULL,
                total_amount REAL NOT NULL,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed' CHECK (status IN ('completed', 'pending', 'cancelled')),
                notes TEXT,
                FOREIGN KEY (buyer_id) REFERENCES users (id),
                FOREIGN KEY (farmer_id) REFERENCES users (id),
                FOREIGN KEY (crop_listing_id) REFERENCES crop_listings (id)
            )
        ''')
        
        # User sessions table for session management
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Market price logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_price_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop_name TEXT NOT NULL,
                old_price REAL,
                new_price REAL NOT NULL,
                old_trend TEXT,
                new_trend TEXT NOT NULL,
                updated_by_user_id INTEGER NOT NULL,
                updated_by_name TEXT NOT NULL,
                updated_by_role TEXT NOT NULL,
                update_reason TEXT,
                update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                price_change_percent REAL,
                FOREIGN KEY (updated_by_user_id) REFERENCES users (id)
            )
        ''')
        
        # Posts table for social media functionality
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                content TEXT NOT NULL,
                media_type TEXT CHECK (media_type IN ('photo', 'video', 'none')),
                media_path TEXT,
                likes_count INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Post comments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Post likes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(post_id, user_id),
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Feedback table for buyers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buyer_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                buyer_id INTEGER NOT NULL,
                farmer_id INTEGER NOT NULL,
                transaction_id INTEGER,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                feedback_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (buyer_id) REFERENCES users (id),
                FOREIGN KEY (farmer_id) REFERENCES users (id),
                FOREIGN KEY (transaction_id) REFERENCES transactions (id)
            )
        ''')
        
        # Weekend farming availability table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekend_farming_availability (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER NOT NULL UNIQUE,
                farmer_name TEXT NOT NULL,
                farmer_phone TEXT,
                location TEXT,
                latitude REAL,
                longitude REAL,
                total_acres REAL NOT NULL,
                available_acres REAL NOT NULL,
                max_people_per_acre INTEGER DEFAULT 5,
                is_open BOOLEAN DEFAULT 1,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farmer_id) REFERENCES users (id)
            )
        ''')
        
        # Weekend farming bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekend_farming_bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id INTEGER NOT NULL,
                booker_id INTEGER NOT NULL,
                booker_name TEXT NOT NULL,
                booker_phone TEXT,
                booking_date DATE NOT NULL,
                people_count INTEGER NOT NULL DEFAULT 1,
                is_group_booking BOOLEAN DEFAULT 0,
                group_leader_name TEXT,
                group_leader_phone TEXT,
                status TEXT DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'cancelled', 'completed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (farmer_id) REFERENCES users (id),
                FOREIGN KEY (booker_id) REFERENCES users (id)
            )
        ''')
        
        # Weekend farming posts table (only for weekend farming participants)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekend_farming_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                content TEXT NOT NULL,
                media_type TEXT CHECK (media_type IN ('photo', 'video', 'none')),
                media_path TEXT,
                likes_count INTEGER DEFAULT 0,
                comments_count INTEGER DEFAULT 0,
                is_hidden BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Weekend farming user roles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekend_farming_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                user_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                can_post BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Weekend farming post likes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekend_farming_post_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(post_id, user_id),
                FOREIGN KEY (post_id) REFERENCES weekend_farming_posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Weekend farming post comments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekend_farming_post_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES weekend_farming_posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Run migrations
        self.run_migrations()
        
        # Create default admin user if doesn't exist
        self.create_default_admin()
        self.create_default_agent()
        self.create_default_weekend_farmer()
        
        # Create sample farm data
        self.create_sample_farm_data()
    
    def run_migrations(self):
        """Run database migrations for schema updates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if location column exists in users table
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'location' not in columns:
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN location TEXT")
                conn.commit()
                print("Migration: Added location column to users table")
            except sqlite3.Error as e:
                print(f"Migration error: {e}")
        
        conn.close()
    
    def create_default_admin(self):
        """Create a default admin user"""
        admin_email = "admin@smartfarm.com"
        admin_password = "admin123"
        
        if not self.get_user_by_email(admin_email):
            self.create_user(
                name="System Administrator",
                email=admin_email,
                password=admin_password,
                role="admin",
                phone="9999999999",
                address="System Admin",
                location="System"
            )
            print(f"Default admin created: {admin_email} / {admin_password}")
    
    def create_default_agent(self):
        """Create a default agent user"""
        agent_email = "agent@smartfarm.com"
        agent_password = "agent123"
        
        if not self.get_user_by_email(agent_email):
            self.create_user(
                name="Farm Agent",
                email=agent_email,
                password=agent_password,
                role="agent",
                phone="8888888888",
                address="Agent Office",
                location="Office"
            )
            print(f"Default agent created: {agent_email} / {agent_password}")
    
    def create_default_weekend_farmer(self):
        """Create a default weekend farmer user"""
        weekend_farmer_email = "weekendfarmer@smartfarm.com"
        weekend_farmer_password = "weekend123"
        
        if not self.get_user_by_email(weekend_farmer_email):
            self.create_user(
                name="Weekend Farmer",
                email=weekend_farmer_email,
                password=weekend_farmer_password,
                role="weekend_farmer",
                phone="7777777777",
                address="Farm Location",
                location="Weekend Farm Area"
            )
            print(f"Default weekend farmer created: {weekend_farmer_email} / {weekend_farmer_password}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, name: str, email: str, password: str, role: str, phone: str = None, address: str = None, location: str = None) -> Optional[int]:
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if user exists with different role
            cursor.execute('SELECT id, role FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # If user exists but wants to add weekend_farmer role
                if role == 'weekend_farmer' and existing_user[1] != 'weekend_farmer':
                    # Update existing user to have weekend_farmer role
                    cursor.execute('''
                        UPDATE users SET role = ? WHERE email = ?
                    ''', (role, email))
                    conn.commit()
                    return existing_user[0]
                else:
                    return None  # User already exists with same role
            
            # Create new user
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, role, phone, address, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, password_hash, role, phone, address, location))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
            SELECT id, name, email, role, phone, address, is_active
            FROM users
            WHERE email = ? AND password_hash = ? AND is_active = 1
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'role': user[3],
                'phone': user[4],
                'address': user[5],
                'is_active': user[6]
            }
        return None
    
    def update_user_profile(self, user_id: int, phone: str, address: str) -> bool:
        """Update user profile information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET phone = ?, address = ?
                WHERE id = ?
            ''', (phone, address, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False
        finally:
            conn.close()
    
    def get_farming_availability(self) -> List[Dict[str, Any]]:
        """Get all available farms for weekend farming"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, farmer_id, farmer_name, location, total_acres, available_acres, max_people_per_acre, is_open, description
            FROM weekend_farming_availability
            WHERE is_open = 1
        ''')
        
        availability = cursor.fetchall()
        conn.close()
        
        return [{
            'id': a[0],
            'farmer_id': a[1],
            'farmer_name': a[2],
            'location': a[3],
            'total_acres': a[4],
            'available_acres': a[5],
            'max_people_per_acre': a[6],
            'is_open': a[7],
            'description': a[8]
        } for a in availability]

    def book_farming_slot(self, farmer_id: int, booker_id: int, booker_name: str, booker_phone: str, booking_date: str, people_count: int, is_group_booking: bool, group_leader_name: Optional[str], group_leader_phone: Optional[str]) -> Optional[int]:
        """Book a slot for weekend farming"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO weekend_farming_bookings (farmer_id, booker_id, booker_name, booker_phone, booking_date, people_count, is_group_booking, group_leader_name, group_leader_phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (farmer_id, booker_id, booker_name, booker_phone, booking_date, people_count, is_group_booking, group_leader_name, group_leader_phone))
            
            booking_id = cursor.lastrowid
            conn.commit()
            return booking_id
        except Exception as e:
            print(f"Error while booking farming slot: {e}")
            return None
        finally:
            conn.close()

    def set_farming_availability(self, farmer_id: int, farmer_name: str, farmer_phone: str, location: str, total_acres: float, available_acres: float, max_people_per_acre: int, is_open: bool, description: Optional[str]) -> bool:
        """Set availability for weekend farming"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # First, check if the farmer already has an entry
            cursor.execute('''
                SELECT id FROM weekend_farming_availability WHERE farmer_id = ?
            ''', (farmer_id,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing entry
                cursor.execute('''
                    UPDATE weekend_farming_availability 
                    SET farmer_name = ?, farmer_phone = ?, location = ?, total_acres = ?, available_acres = ?, max_people_per_acre = ?, is_open = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE farmer_id = ?
                ''', (farmer_name, farmer_phone, location, total_acres, available_acres, max_people_per_acre, is_open, description, farmer_id))
            else:
                # Insert new entry
                cursor.execute('''
                    INSERT INTO weekend_farming_availability (farmer_id, farmer_name, farmer_phone, location, total_acres, available_acres, max_people_per_acre, is_open, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (farmer_id, farmer_name, farmer_phone, location, total_acres, available_acres, max_people_per_acre, is_open, description))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error setting farming availability: {e}")
            return False
        finally:
            conn.close()

    def toggle_farming_post_right(self, user_id: int, user_name: str, email: str, phone: str, can_post: bool) -> bool:
        """Toggle user's right to post in the weekend farming community"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if the user already exists
            cursor.execute('''
                SELECT id FROM weekend_farming_users WHERE user_id = ?
            ''', (user_id,))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing entry
                cursor.execute('''
                    UPDATE weekend_farming_users 
                    SET can_post = ?
                    WHERE user_id = ?
                ''', (can_post, user_id))
            else:
                # Insert new entry
                cursor.execute('''
                    INSERT INTO weekend_farming_users (user_id, user_name, email, phone, can_post)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, user_name, email, phone, can_post))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error toggling farming post right: {e}")
            return False
        finally:
            conn.close()

    def get_farmer_availability(self, farmer_id: int) -> Optional[Dict[str, Any]]:
        """Get farmer's weekend farming availability"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, farmer_id, farmer_name, farmer_phone, location, total_acres, available_acres, max_people_per_acre, is_open, description
            FROM weekend_farming_availability
            WHERE farmer_id = ?
        ''', (farmer_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'farmer_id': result[1],
                'farmer_name': result[2],
                'farmer_phone': result[3],
                'location': result[4],
                'total_acres': result[5],
                'available_acres': result[6],
                'max_people_per_acre': result[7],
                'is_open': result[8],
                'description': result[9]
            }
        return None

    def get_farmer_bookings(self, farmer_id: int) -> List[Dict[str, Any]]:
        """Get all bookings for a farmer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, booker_id, booker_name, booker_phone, booking_date, people_count, is_group_booking, group_leader_name, group_leader_phone, status
            FROM weekend_farming_bookings
            WHERE farmer_id = ? AND status != 'cancelled'
            ORDER BY booking_date DESC
        ''', (farmer_id,))
        
        bookings = cursor.fetchall()
        conn.close()
        
        return [{
            'id': b[0],
            'booker_id': b[1],
            'booker_name': b[2],
            'booker_phone': b[3],
            'booking_date': b[4],
            'people_count': b[5],
            'is_group_booking': b[6],
            'group_leader_name': b[7],
            'group_leader_phone': b[8],
            'status': b[9]
        } for b in bookings]

    def get_user_bookings(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all bookings made by a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT b.id, b.farmer_id, a.farmer_name, a.location, b.booking_date, b.people_count, b.is_group_booking, b.status
            FROM weekend_farming_bookings b
            JOIN weekend_farming_availability a ON b.farmer_id = a.farmer_id
            WHERE b.booker_id = ?
            ORDER BY b.booking_date DESC
        ''', (user_id,))
        
        bookings = cursor.fetchall()
        conn.close()
        
        return [{
            'id': b[0],
            'farmer_id': b[1],
            'farmer_name': b[2],
            'location': b[3],
            'booking_date': b[4],
            'people_count': b[5],
            'is_group_booking': b[6],
            'status': b[7]
        } for b in bookings]

    def check_booking_capacity(self, farmer_id: int, booking_date: str, people_count: int) -> bool:
        """Check if farm has capacity for the booking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get farm capacity
        cursor.execute('''
            SELECT available_acres, max_people_per_acre
            FROM weekend_farming_availability
            WHERE farmer_id = ? AND is_open = 1
        ''', (farmer_id,))
        
        capacity_result = cursor.fetchone()
        if not capacity_result:
            conn.close()
            return False
        
        available_acres, max_people_per_acre = capacity_result
        max_capacity = int(available_acres * max_people_per_acre)
        
        # Get current bookings for the date
        cursor.execute('''
            SELECT SUM(people_count)
            FROM weekend_farming_bookings
            WHERE farmer_id = ? AND booking_date = ? AND status = 'confirmed'
        ''', (farmer_id, booking_date))
        
        current_bookings = cursor.fetchone()[0] or 0
        conn.close()
        
        return (current_bookings + people_count) <= max_capacity

    def can_user_post_weekend_farming(self, user_id: int) -> bool:
        """Check if user can post in weekend farming community"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user has any confirmed bookings
        cursor.execute('''
            SELECT COUNT(*)
            FROM weekend_farming_bookings
            WHERE booker_id = ? AND status = 'confirmed'
        ''', (user_id,))
        
        has_bookings = cursor.fetchone()[0] > 0
        
        # Check if user is in weekend farming users with posting rights
        cursor.execute('''
            SELECT can_post
            FROM weekend_farming_users
            WHERE user_id = ?
        ''', (user_id,))
        
        post_rights = cursor.fetchone()
        can_post_explicit = post_rights[0] if post_rights else True
        
        # Check if user has weekend_farmer role
        cursor.execute('''
            SELECT role FROM users WHERE id = ?
        ''', (user_id,))
        
        user_role = cursor.fetchone()
        is_weekend_farmer = user_role and user_role[0] == 'weekend_farmer'
        
        conn.close()
        
        return is_weekend_farmer and can_post_explicit
    
    def get_weekend_farming_posts(self, show_hidden: bool = False) -> List[tuple]:
        """Get all weekend farming posts with media support"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if show_hidden:
            cursor.execute('''
                SELECT id, user_id, user_name, content, media_type, media_path, 
                       likes_count, comments_count, is_hidden, created_at
                FROM weekend_farming_posts
                ORDER BY created_at DESC
            ''')
        else:
            cursor.execute('''
                SELECT id, user_id, user_name, content, media_type, media_path, 
                       likes_count, comments_count, is_hidden, created_at
                FROM weekend_farming_posts
                WHERE is_hidden = 0
                ORDER BY created_at DESC
            ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        return posts
    
    def toggle_post_visibility(self, post_id: int, is_hidden: bool) -> bool:
        """Toggle post visibility"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE weekend_farming_posts SET is_hidden = ? WHERE id = ?",
                (is_hidden, post_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error toggling post visibility: {e}")
            return False
        finally:
            conn.close()
    
    def delete_post(self, post_id: int) -> bool:
        """Delete a weekend farming post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM weekend_farming_posts WHERE id = ?", (post_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False
        finally:
            conn.close()
    
    def get_favorite_farmers(self, user_id: int) -> List[Dict[str, Any]]:
        """Get favorite farmers for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create favorites table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_favorite_farmers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                farmer_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, farmer_id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (farmer_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            SELECT wfa.id, wfa.farmer_id, wfa.farmer_name, wfa.location, wfa.total_acres, 
                   wfa.available_acres, wfa.max_people_per_acre, wfa.is_open, wfa.description
            FROM user_favorite_farmers uff
            JOIN weekend_farming_availability wfa ON uff.farmer_id = wfa.farmer_id
            WHERE uff.user_id = ?
        ''', (user_id,))
        
        favorites = cursor.fetchall()
        conn.close()
        
        return [{
            'id': f[0],
            'farmer_id': f[1],
            'farmer_name': f[2],
            'location': f[3],
            'total_acres': f[4],
            'available_acres': f[5],
            'max_people_per_acre': f[6],
            'is_open': f[7],
            'description': f[8]
        } for f in favorites]
    
    def add_favorite_farmer(self, user_id: int, farmer_id: int) -> bool:
        """Add a farmer to user's favorites"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO user_favorite_farmers (user_id, farmer_id)
                VALUES (?, ?)
            ''', (user_id, farmer_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding favorite farmer: {e}")
            return False
        finally:
            conn.close()
    
    def remove_favorite_farmer(self, user_id: int, farmer_id: int) -> bool:
        """Remove a farmer from user's favorites"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM user_favorite_farmers 
                WHERE user_id = ? AND farmer_id = ?
            ''', (user_id, farmer_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error removing favorite farmer: {e}")
            return False
        finally:
            conn.close()
    
    def like_weekend_farming_post(self, post_id: int, user_id: int) -> bool:
        """Like or unlike a weekend farming post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if user already liked this post
            cursor.execute('''
                SELECT id FROM weekend_farming_post_likes 
                WHERE post_id = ? AND user_id = ?
            ''', (post_id, user_id))
            
            existing_like = cursor.fetchone()
            
            if existing_like:
                # Unlike the post
                cursor.execute('''
                    DELETE FROM weekend_farming_post_likes 
                    WHERE post_id = ? AND user_id = ?
                ''', (post_id, user_id))
                
                cursor.execute('''
                    UPDATE weekend_farming_posts 
                    SET likes_count = likes_count - 1 
                    WHERE id = ?
                ''', (post_id,))
                
                conn.commit()
                return False  # Unliked
            else:
                # Like the post
                cursor.execute('''
                    INSERT INTO weekend_farming_post_likes (post_id, user_id) 
                    VALUES (?, ?)
                ''', (post_id, user_id))
                
                cursor.execute('''
                    UPDATE weekend_farming_posts 
                    SET likes_count = likes_count + 1 
                    WHERE id = ?
                ''', (post_id,))
                
                conn.commit()
                return True  # Liked
        except Exception as e:
            print(f"Error liking post: {e}")
            return False
        finally:
            conn.close()
    
    def add_weekend_farming_comment(self, post_id: int, user_id: int, user_name: str, comment: str) -> bool:
        """Add a comment to a weekend farming post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO weekend_farming_post_comments (post_id, user_id, user_name, comment) 
                VALUES (?, ?, ?, ?)
            ''', (post_id, user_id, user_name, comment))
            
            cursor.execute('''
                UPDATE weekend_farming_posts 
                SET comments_count = comments_count + 1 
                WHERE id = ?
            ''', (post_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding comment: {e}")
            return False
        finally:
            conn.close()
    
    def get_weekend_farming_comments(self, post_id: int) -> List[tuple]:
        """Get comments for a weekend farming post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_name, comment, created_at
            FROM weekend_farming_post_comments
            WHERE post_id = ?
            ORDER BY created_at ASC
        ''', (post_id,))
        
        comments = cursor.fetchall()
        conn.close()
        
        return comments
    
    def create_weekend_farming_post(self, user_id: int, user_name: str, content: str, media_type: str = 'none', media_path: Optional[str] = None) -> bool:
        """Create a new weekend farming post with media support"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO weekend_farming_posts (user_id, user_name, content, media_type, media_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_name, content, media_type, media_path))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating weekend farming post: {e}")
            return False
        finally:
            conn.close()
    
    def update_user_status(self, user_id: int, is_active: bool) -> bool:
        """Update user active status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET is_active = ?
                WHERE id = ?
            ''', (is_active, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user status: {e}")
            return False
        finally:
            conn.close()
    
    def create_sample_farm_data(self):
        """Create sample farm data for testing"""
        sample_farms = [
            (1, "John Smith", "9876543210", "Bangalore Rural", 10.5, 10.5, 5, True, "Organic farming with weekend experience programs"),
            (2, "Mary Johnson", "9876543211", "Mysore District", 8.2, 8.2, 4, True, "Traditional farming methods with hands-on learning"),
            (3, "David Brown", "9876543212", "Mandya", 15.0, 15.0, 6, True, "Large farm with multiple crop varieties"),
            (4, "Sarah Davis", "9876543213", "Hassan", 6.8, 6.8, 3, False, "Small family farm with personalized experience"),
            (5, "Mike Wilson", "9876543214", "Tumkur", 12.3, 12.3, 5, True, "Modern farming techniques demonstration")
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for farm in sample_farms:
                farmer_id, farmer_name, farmer_phone, location, total_acres, available_acres, max_people_per_acre, is_open, description = farm
                
                # Check if farm already exists
                cursor.execute('SELECT id FROM weekend_farming_availability WHERE farmer_id = ?', (farmer_id,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO weekend_farming_availability 
                        (farmer_id, farmer_name, farmer_phone, location, total_acres, available_acres, max_people_per_acre, is_open, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', farm)
            
            conn.commit()
            print("Sample farm data created successfully")
            return True
        except Exception as e:
            print(f"Error creating sample farm data: {e}")
            return False
        finally:
            conn.close()

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, role, phone, address, is_active
            FROM users
            WHERE email = ?
        ''', (email,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'role': user[3],
                'phone': user[4],
                'address': user[5],
                'is_active': user[6]
            }
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, role, phone, address, is_active
            FROM users
            WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'role': user[3],
                'phone': user[4],
                'address': user[5],
                'is_active': user[6]
            }
        return None
    
    def get_user_location(self, user_id: int) -> Optional[str]:
        """Get user's location from address or location field"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT address, location FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                address, location = result
                # Prefer address over location field
                return address or location
            return None
        except Exception as e:
            print(f"Error getting user location: {e}")
            return None
    
    def update_user_address(self, user_id: int, address: str) -> bool:
        """Update user's address"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE users SET address = ? WHERE id = ?",
                (address, user_id)
            )
            
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            
            return success
        except Exception as e:
            print(f"Error updating user address: {e}")
            return False
    
    def create_crop_listing(self, farmer_id: int, crop_name: str, quantity: float, 
                          expected_price: float, description: str = None, location: str = None,
                          farmer_name: str = None, farmer_phone: str = None, agent_id: int = None) -> Optional[int]:
        """Create a new crop listing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO crop_listings (farmer_id, crop_name, quantity, expected_price, description, location, farmer_name, farmer_phone, agent_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (farmer_id, crop_name, quantity, expected_price, description, location, farmer_name, farmer_phone, agent_id))
            
            listing_id = cursor.lastrowid
            conn.commit()
            return listing_id
        except Exception as e:
            print(f"Error creating crop listing: {e}")
            return None
        finally:
            conn.close()
    
    def get_crop_listings(self, status: str = 'available') -> List[Dict[str, Any]]:
        """Get all crop listings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cl.id, cl.farmer_id, 
                   COALESCE(cl.farmer_name, u.name) as farmer_name, 
                   COALESCE(cl.farmer_phone, u.phone) as farmer_phone, 
                   cl.crop_name, cl.quantity, cl.expected_price, cl.description, 
                   cl.location, cl.status, cl.created_at, cl.updated_at, cl.agent_id
            FROM crop_listings cl
            LEFT JOIN users u ON cl.farmer_id = u.id
            WHERE cl.status = ?
            ORDER BY cl.created_at DESC
        ''', (status,))
        
        listings = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': listing[0],
                'farmer_id': listing[1],
                'farmer_name': listing[2],
                'farmer_phone': listing[3],
                'crop_name': listing[4],
                'quantity': listing[5],
                'expected_price': listing[6],
                'description': listing[7],
                'location': listing[8],
                'status': listing[9],
                'created_at': listing[10],
                'updated_at': listing[11],
                'agent_id': listing[12]
            }
            for listing in listings
        ]
    
    def get_farmer_listings(self, farmer_id: int) -> List[Dict[str, Any]]:
        """Get crop listings for a specific farmer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, crop_name, quantity, expected_price, description, location, status, created_at
            FROM crop_listings
            WHERE farmer_id = ?
            ORDER BY created_at DESC
        ''', (farmer_id,))
        
        listings = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': listing[0],
                'crop_name': listing[1],
                'quantity': listing[2],
                'expected_price': listing[3],
                'description': listing[4],
                'location': listing[5],
                'status': listing[6],
                'created_at': listing[7]
            }
            for listing in listings
        ]
    
    def get_agent_listings(self, agent_id: int) -> List[Dict[str, Any]]:
        """Get crop listings created by a specific agent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, crop_name, quantity, expected_price, description, location, status, 
                   created_at, farmer_name, farmer_phone
            FROM crop_listings
            WHERE agent_id = ?
            ORDER BY created_at DESC
        ''', (agent_id,))
        
        listings = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': listing[0],
                'crop_name': listing[1],
                'quantity': listing[2],
                'expected_price': listing[3],
                'description': listing[4],
                'location': listing[5],
                'status': listing[6],
                'created_at': listing[7],
                'farmer_name': listing[8],
                'farmer_phone': listing[9]
            }
            for listing in listings
        ]
    
    def create_buyer_offer(self, buyer_id: int, crop_listing_id: int, crop_name: str,
                          offer_price: float, quantity_wanted: float, notes: str = None) -> Optional[int]:
        """Create a new buyer offer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO buyer_offers (buyer_id, crop_listing_id, crop_name, offer_price, quantity_wanted, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (buyer_id, crop_listing_id, crop_name, offer_price, quantity_wanted, notes))
            
            offer_id = cursor.lastrowid
            conn.commit()
            return offer_id
        except Exception as e:
            print(f"Error creating buyer offer: {e}")
            return None
        finally:
            conn.close()
    
    def get_buyer_offers(self, buyer_id: int = None) -> List[Dict[str, Any]]:
        """Get buyer offers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if buyer_id:
            cursor.execute('''
                SELECT bo.id, bo.buyer_id, u.name as buyer_name, bo.crop_listing_id, 
                       bo.crop_name, bo.offer_price, bo.quantity_wanted, bo.notes, 
                       bo.status, bo.created_at
                FROM buyer_offers bo
                JOIN users u ON bo.buyer_id = u.id
                WHERE bo.buyer_id = ?
                ORDER BY bo.created_at DESC
            ''', (buyer_id,))
        else:
            cursor.execute('''
                SELECT bo.id, bo.buyer_id, u.name as buyer_name, bo.crop_listing_id, 
                       bo.crop_name, bo.offer_price, bo.quantity_wanted, bo.notes, 
                       bo.status, bo.created_at
                FROM buyer_offers bo
                JOIN users u ON bo.buyer_id = u.id
                ORDER BY bo.created_at DESC
            ''')
        
        offers = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': offer[0],
                'buyer_id': offer[1],
                'buyer_name': offer[2],
                'crop_listing_id': offer[3],
                'crop_name': offer[4],
                'offer_price': offer[5],
                'quantity_wanted': offer[6],
                'notes': offer[7],
                'status': offer[8],
                'created_at': offer[9]
            }
            for offer in offers
        ]
    
    def get_offers_for_farmer(self, farmer_id: int) -> List[Dict[str, Any]]:
        """Get all offers for a farmer's listings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT bo.id, bo.buyer_id, u.name as buyer_name, u.phone as buyer_phone,
                   bo.crop_listing_id, bo.crop_name, bo.offer_price, bo.quantity_wanted, 
                   bo.notes, bo.status, bo.created_at, cl.expected_price
            FROM buyer_offers bo
            JOIN users u ON bo.buyer_id = u.id
            JOIN crop_listings cl ON bo.crop_listing_id = cl.id
            WHERE cl.farmer_id = ?
            ORDER BY bo.created_at DESC
        ''', (farmer_id,))
        
        offers = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': offer[0],
                'buyer_id': offer[1],
                'buyer_name': offer[2],
                'buyer_phone': offer[3],
                'crop_listing_id': offer[4],
                'crop_name': offer[5],
                'offer_price': offer[6],
                'quantity_wanted': offer[7],
                'notes': offer[8],
                'status': offer[9],
                'created_at': offer[10],
                'expected_price': offer[11]
            }
            for offer in offers
        ]
    
    def get_offers_for_agent(self, agent_id: int) -> List[Dict[str, Any]]:
        """Get all offers for agent's farmer listings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT bo.id, bo.buyer_id, u.name as buyer_name, u.phone as buyer_phone,
                   bo.crop_listing_id, bo.crop_name, bo.offer_price, bo.quantity_wanted, 
                   bo.notes, bo.status, bo.created_at, cl.expected_price, cl.farmer_name, cl.farmer_phone
            FROM buyer_offers bo
            JOIN users u ON bo.buyer_id = u.id
            JOIN crop_listings cl ON bo.crop_listing_id = cl.id
            WHERE cl.agent_id = ?
            ORDER BY bo.created_at DESC
        ''', (agent_id,))
        
        offers = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': offer[0],
                'buyer_id': offer[1],
                'buyer_name': offer[2],
                'buyer_phone': offer[3],
                'crop_listing_id': offer[4],
                'crop_name': offer[5],
                'offer_price': offer[6],
                'quantity_wanted': offer[7],
                'notes': offer[8],
                'status': offer[9],
                'created_at': offer[10],
                'expected_price': offer[11],
                'farmer_name': offer[12],
                'farmer_phone': offer[13]
            }
            for offer in offers
        ]
    
    def get_offers_by_status(self, status: str = None) -> List[Dict[str, Any]]:
        """Get offers by status (for admin dashboard)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT bo.id, bo.buyer_id, ub.name as buyer_name, ub.phone as buyer_phone,
                       bo.crop_listing_id, bo.crop_name, bo.offer_price, bo.quantity_wanted, 
                       bo.notes, bo.status, bo.created_at, cl.expected_price,
                       COALESCE(cl.farmer_name, uf.name) as farmer_name,
                       COALESCE(cl.farmer_phone, uf.phone) as farmer_phone,
                       ua.name as agent_name
                FROM buyer_offers bo
                JOIN users ub ON bo.buyer_id = ub.id
                JOIN crop_listings cl ON bo.crop_listing_id = cl.id
                LEFT JOIN users uf ON cl.farmer_id = uf.id
                LEFT JOIN users ua ON cl.agent_id = ua.id
                WHERE bo.status = ?
                ORDER BY bo.created_at DESC
            ''', (status,))
        else:
            cursor.execute('''
                SELECT bo.id, bo.buyer_id, ub.name as buyer_name, ub.phone as buyer_phone,
                       bo.crop_listing_id, bo.crop_name, bo.offer_price, bo.quantity_wanted, 
                       bo.notes, bo.status, bo.created_at, cl.expected_price,
                       COALESCE(cl.farmer_name, uf.name) as farmer_name,
                       COALESCE(cl.farmer_phone, uf.phone) as farmer_phone,
                       ua.name as agent_name
                FROM buyer_offers bo
                JOIN users ub ON bo.buyer_id = ub.id
                JOIN crop_listings cl ON bo.crop_listing_id = cl.id
                LEFT JOIN users uf ON cl.farmer_id = uf.id
                LEFT JOIN users ua ON cl.agent_id = ua.id
                ORDER BY bo.created_at DESC
            ''')
        
        offers = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': offer[0],
                'buyer_id': offer[1],
                'buyer_name': offer[2],
                'buyer_phone': offer[3],
                'crop_listing_id': offer[4],
                'crop_name': offer[5],
                'offer_price': offer[6],
                'quantity_wanted': offer[7],
                'notes': offer[8],
                'status': offer[9],
                'created_at': offer[10],
                'expected_price': offer[11],
                'farmer_name': offer[12],
                'farmer_phone': offer[13],
                'agent_name': offer[14]
            }
            for offer in offers
        ]
    
    
    def update_market_price(self, crop_name: str, price: float, trend: str, updated_by_user: dict = None, reason: str = None) -> bool:
        """Update market price for a crop with enhanced logging"""
        try:
            import pandas as pd
            import os
            import tempfile
            import shutil
            
            # Market price logs table is now initialized in init_database()
            
            csv_path = 'data/market_prices.csv'
            if os.path.exists(csv_path):
                # Read the current data
                df = pd.read_csv(csv_path)
                
                # Store old values for logging
                old_price = None
                old_trend = None
                price_change_percent = 0
                
                # Update existing crop or add new one
                crop_index = df[df['Crop'].str.lower() == crop_name.lower()].index
                if len(crop_index) > 0:
                    # Get old values
                    old_price = float(df.loc[crop_index[0], 'Price'])
                    old_trend = str(df.loc[crop_index[0], 'Trend'])
                    
                    # Calculate price change percentage
                    if old_price > 0:
                        price_change_percent = round(((price - old_price) / old_price) * 100, 2)
                    
                    # Update values
                    df.loc[crop_index[0], 'Price'] = price
                    df.loc[crop_index[0], 'Trend'] = trend
                    df.loc[crop_index[0], 'Last_Updated'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                else:
                    # Add new crop
                    new_row = {
                        'Crop': crop_name.lower(),
                        'Price': price,
                        'Unit': 'quintal',
                        'Trend': trend,
                        'Last_Updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                
                # Try to write to a temporary file first, then replace
                try:
                    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
                        tmp_path = tmp_file.name
                        df.to_csv(tmp_path, index=False)
                    
                    # Replace the original file
                    shutil.move(tmp_path, csv_path)
                    
                    # Log the price update in database
                    if updated_by_user:
                        self.log_market_price_update(
                            crop_name=crop_name,
                            old_price=old_price,
                            new_price=price,
                            old_trend=old_trend,
                            new_trend=trend,
                            updated_by_user=updated_by_user,
                            reason=reason,
                            price_change_percent=price_change_percent
                        )
                    
                    return True
                except:
                    # Fallback: try direct write
                    df.to_csv(csv_path, index=False)
                    
                    # Log the price update in database
                    if updated_by_user:
                        self.log_market_price_update(
                            crop_name=crop_name,
                            old_price=old_price,
                            new_price=price,
                            old_trend=old_trend,
                            new_trend=trend,
                            updated_by_user=updated_by_user,
                            reason=reason,
                            price_change_percent=price_change_percent
                        )
                    
                    return True
            return False
        except Exception as e:
            print(f"Error updating market price: {e}")
            return False
    
    def log_market_price_update(self, crop_name: str, old_price: float, new_price: float, 
                               old_trend: str, new_trend: str, updated_by_user: dict, 
                               reason: str = None, price_change_percent: float = 0) -> bool:
        """Log market price update to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO market_price_logs (
                    crop_name, old_price, new_price, old_trend, new_trend,
                    updated_by_user_id, updated_by_name, updated_by_role,
                    update_reason, price_change_percent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                crop_name.lower(),
                old_price,
                new_price,
                old_trend,
                new_trend,
                updated_by_user['id'],
                updated_by_user['name'],
                updated_by_user['role'],
                reason,
                price_change_percent
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging market price update: {e}")
            return False
        finally:
            conn.close()
    
    def get_market_price_logs(self, limit: int = 50, crop_name: str = None) -> List[Dict[str, Any]]:
        """Get market price update logs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if crop_name:
            cursor.execute('''
                SELECT id, crop_name, old_price, new_price, old_trend, new_trend,
                       updated_by_name, updated_by_role, update_reason, 
                       update_timestamp, price_change_percent
                FROM market_price_logs
                WHERE crop_name = ?
                ORDER BY update_timestamp DESC
                LIMIT ?
            ''', (crop_name.lower(), limit))
        else:
            cursor.execute('''
                SELECT id, crop_name, old_price, new_price, old_trend, new_trend,
                       updated_by_name, updated_by_role, update_reason, 
                       update_timestamp, price_change_percent
                FROM market_price_logs
                ORDER BY update_timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        logs = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': log[0],
                'crop_name': log[1],
                'old_price': log[2],
                'new_price': log[3],
                'old_trend': log[4],
                'new_trend': log[5],
                'updated_by_name': log[6],
                'updated_by_role': log[7],
                'update_reason': log[8],
                'update_timestamp': log[9],
                'price_change_percent': log[10]
            }
            for log in logs
        ]
    
    def get_recent_price_changes(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get recent price changes within specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT crop_name, old_price, new_price, old_trend, new_trend,
                   updated_by_name, updated_by_role, update_timestamp, 
                   price_change_percent
            FROM market_price_logs
            WHERE update_timestamp >= datetime('now', '-{} days')
            ORDER BY update_timestamp DESC
        '''.format(days))
        
        changes = cursor.fetchall()
        conn.close()
        
        return [
            {
                'crop_name': change[0],
                'old_price': change[1],
                'new_price': change[2],
                'old_trend': change[3],
                'new_trend': change[4],
                'updated_by_name': change[5],
                'updated_by_role': change[6],
                'update_timestamp': change[7],
                'price_change_percent': change[8]
            }
            for change in changes
        ]
    
    def get_farmers_for_notification(self, crop_name: str = None) -> List[Dict[str, Any]]:
        """Get farmers to notify about market price updates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if crop_name:
            # Get farmers who have listings for the specific crop
            cursor.execute('''
                SELECT DISTINCT u.id, u.name, u.phone, u.email
                FROM users u
                JOIN crop_listings cl ON u.id = cl.farmer_id OR cl.farmer_phone = u.phone
                WHERE u.role = 'farmer' AND u.is_active = 1 AND u.phone IS NOT NULL
                    AND (cl.crop_name = ? OR cl.farmer_phone IS NOT NULL)
                ORDER BY u.name
            ''', (crop_name.lower(),))
        else:
            # Get all active farmers with phone numbers
            cursor.execute('''
                SELECT id, name, phone, email
                FROM users
                WHERE role = 'farmer' AND is_active = 1 AND phone IS NOT NULL
                ORDER BY name
            ''')
        
        farmers = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': farmer[0],
                'name': farmer[1],
                'phone': farmer[2],
                'email': farmer[3]
            }
            for farmer in farmers
        ]
    
    def create_transaction(self, buyer_id: int, farmer_id: int, crop_listing_id: int,
                          crop_name: str, quantity: float, price_per_unit: float, 
                          total_amount: float, notes: str = None) -> Optional[int]:
        """Create a new transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO transactions (buyer_id, farmer_id, crop_listing_id, crop_name, 
                                        quantity, price_per_unit, total_amount, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (buyer_id, farmer_id, crop_listing_id, crop_name, quantity, price_per_unit, total_amount, notes))
            
            transaction_id = cursor.lastrowid
            conn.commit()
            return transaction_id
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (for admin)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, email, role, phone, address, is_active, created_at
            FROM users
            ORDER BY created_at DESC
        ''')
        
        users = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'role': user[3],
                'phone': user[4],
                'address': user[5],
                'is_active': user[6],
                'created_at': user[7]
            }
            for user in users
        ]
    
    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """Get all transactions (for admin)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.buyer_id, ub.name as buyer_name, t.farmer_id, uf.name as farmer_name,
                   t.crop_name, t.quantity, t.price_per_unit, t.total_amount, t.transaction_date, t.status
            FROM transactions t
            JOIN users ub ON t.buyer_id = ub.id
            JOIN users uf ON t.farmer_id = uf.id
            ORDER BY t.transaction_date DESC
        ''')
        
        transactions = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': transaction[0],
                'buyer_id': transaction[1],
                'buyer_name': transaction[2],
                'farmer_id': transaction[3],
                'farmer_name': transaction[4],
                'crop_name': transaction[5],
                'quantity': transaction[6],
                'price_per_unit': transaction[7],
                'total_amount': transaction[8],
                'transaction_date': transaction[9],
                'status': transaction[10]
            }
            for transaction in transactions
        ]
    
    def update_user_status(self, user_id: int, is_active: bool) -> bool:
        """Update user active status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET is_active = ? WHERE id = ?
            ''', (is_active, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user status: {e}")
            return False
        finally:
            conn.close()
    
    def update_crop_listing_status(self, listing_id: int, status: str) -> bool:
        """Update crop listing status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE crop_listings SET status = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (status, listing_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating crop listing status: {e}")
            return False
        finally:
            conn.close()
    
    def update_offer_status(self, offer_id: int, status: str) -> bool:
        """Update offer status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE buyer_offers SET status = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (status, offer_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating offer status: {e}")
            return False
        finally:
            conn.close()
    
    def get_offer_details(self, offer_id: int) -> Optional[Dict[str, Any]]:
        """Get offer details by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT bo.id, bo.buyer_id, bo.crop_listing_id, bo.crop_name, 
                   bo.offer_price, bo.quantity_wanted, bo.notes, bo.status,
                   cl.farmer_id, cl.quantity as available_quantity, cl.expected_price
            FROM buyer_offers bo
            JOIN crop_listings cl ON bo.crop_listing_id = cl.id
            WHERE bo.id = ?
        ''', (offer_id,))
        
        offer = cursor.fetchone()
        conn.close()
        
        if offer:
            return {
                'id': offer[0],
                'buyer_id': offer[1],
                'crop_listing_id': offer[2],
                'crop_name': offer[3],
                'offer_price': offer[4],
                'quantity_wanted': offer[5],
                'notes': offer[6],
                'status': offer[7],
                'farmer_id': offer[8],
                'available_quantity': offer[9],
                'expected_price': offer[10]
            }
        return None
    
    def accept_offer(self, offer_id: int) -> bool:
        """Accept an offer and create transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get offer details
            offer = self.get_offer_details(offer_id)
            if not offer:
                return False
            
            # Update offer status to accepted
            cursor.execute('''
                UPDATE buyer_offers SET status = 'accepted', updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (offer_id,))
            
            # Create transaction
            total_amount = offer['offer_price'] * offer['quantity_wanted']
            cursor.execute('''
                INSERT INTO transactions (buyer_id, farmer_id, crop_listing_id, crop_name, 
                                        quantity, price_per_unit, total_amount, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (offer['buyer_id'], offer['farmer_id'], offer['crop_listing_id'], 
                  offer['crop_name'], offer['quantity_wanted'], offer['offer_price'], 
                  total_amount, f"Accepted offer - {offer['notes']}"))
            
            # Update crop listing - reduce quantity or mark as sold
            remaining_quantity = offer['available_quantity'] - offer['quantity_wanted']
            if remaining_quantity <= 0:
                cursor.execute('''
                    UPDATE crop_listings SET status = 'sold', updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (offer['crop_listing_id'],))
            else:
                cursor.execute('''
                    UPDATE crop_listings SET quantity = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (remaining_quantity, offer['crop_listing_id']))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error accepting offer: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total users by role
        cursor.execute('SELECT role, COUNT(*) FROM users WHERE is_active = 1 GROUP BY role')
        user_stats = dict(cursor.fetchall())
        
        # Total active crop listings
        cursor.execute('SELECT COUNT(*) FROM crop_listings WHERE status = "available"')
        active_listings = cursor.fetchone()[0]
        
        # Total transactions
        cursor.execute('SELECT COUNT(*) FROM transactions')
        total_transactions = cursor.fetchone()[0]
        
        # Total transaction value
        cursor.execute('SELECT SUM(total_amount) FROM transactions')
        total_value = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_farmers': user_stats.get('farmer', 0),
            'total_buyers': user_stats.get('buyer', 0),
            'total_agents': user_stats.get('agent', 0),
            'total_admins': user_stats.get('admin', 0),
            'active_listings': active_listings,
            'total_transactions': total_transactions,
            'total_transaction_value': total_value
        }
    
    def create_post(self, user_id: int, user_name: str, content: str, media_type: str = 'none', media_path: str = None) -> Optional[int]:
        """Create a new post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO posts (user_id, user_name, content, media_type, media_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_name, content, media_type, media_path))
            
            post_id = cursor.lastrowid
            conn.commit()
            return post_id
        except Exception as e:
            print(f"Error creating post: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """Get all posts ordered by creation date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, user_name, content, media_type, media_path, 
                   likes_count, comments_count, created_at
            FROM posts
            ORDER BY created_at DESC
        ''')
        
        posts = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': post[0],
                'user_id': post[1],
                'user_name': post[2],
                'content': post[3],
                'media_type': post[4],
                'media_path': post[5],
                'likes_count': post[6],
                'comments_count': post[7],
                'created_at': post[8]
            }
            for post in posts
        ]
    
    def get_post_comments(self, post_id: int) -> List[Dict[str, Any]]:
        """Get comments for a specific post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, user_name, comment, created_at
            FROM post_comments
            WHERE post_id = ?
            ORDER BY created_at ASC
        ''', (post_id,))
        
        comments = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': comment[0],
                'user_id': comment[1],
                'user_name': comment[2],
                'comment': comment[3],
                'created_at': comment[4]
            }
            for comment in comments
        ]
    
    def add_comment_to_post(self, post_id: int, user_id: int, user_name: str, comment: str) -> Optional[int]:
        """Add a comment to a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO post_comments (post_id, user_id, user_name, comment)
                VALUES (?, ?, ?, ?)
            ''', (post_id, user_id, user_name, comment))
            
            comment_id = cursor.lastrowid
            cursor.execute('''
                UPDATE posts SET comments_count = comments_count + 1 WHERE id = ?
            ''', (post_id,))
            
            conn.commit()
            return comment_id
        except Exception as e:
            print(f"Error adding comment: {e}")
            return None
        finally:
            conn.close()
    
    def like_post(self, post_id: int, user_id: int) -> bool:
        """Like a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO post_likes (post_id, user_id) VALUES (?, ?)
            ''', (post_id, user_id))
            
            cursor.execute('''
                UPDATE posts SET likes_count = likes_count + 1 WHERE id = ?
            ''', (post_id,))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # User already liked this post
        except Exception as e:
            print(f"Error liking post: {e}")
            return False
        finally:
            conn.close()
    
    def has_user_liked_post(self, post_id: int, user_id: int) -> bool:
        """Check if user has already liked a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM post_likes WHERE post_id = ? AND user_id = ?
        ''', (post_id, user_id))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def give_feedback(self, buyer_id: int, farmer_id: int, transaction_id: int = None, rating: int = 5, feedback_text: str = None) -> Optional[int]:
        """Give feedback for a transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO buyer_feedback (buyer_id, farmer_id, transaction_id, rating, feedback_text)
                VALUES (?, ?, ?, ?, ?)
            ''', (buyer_id, farmer_id, transaction_id, rating, feedback_text))
            
            feedback_id = cursor.lastrowid
            conn.commit()
            return feedback_id
        except Exception as e:
            print(f"Error giving feedback: {e}")
            return None
        finally:
            conn.close()
    
    def get_farmer_feedback(self, farmer_id: int) -> List[Dict[str, Any]]:
        """Get all feedback for a farmer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT bf.id, bf.buyer_id, ub.name as buyer_name, bf.rating, bf.feedback_text, bf.created_at
            FROM buyer_feedback bf
            JOIN users ub ON bf.buyer_id = ub.id
            WHERE bf.farmer_id = ?
            ORDER BY bf.created_at DESC
        ''', (farmer_id,))
        
        feedback_list = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': feedback[0],
                'buyer_id': feedback[1],
                'buyer_name': feedback[2],
                'rating': feedback[3],
                'feedback_text': feedback[4],
                'created_at': feedback[5]
            }
            for feedback in feedback_list
        ]
    
    def get_buyer_transactions(self, buyer_id: int) -> List[Dict[str, Any]]:
        """Get all transactions for a specific buyer"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.buyer_id, t.farmer_id, uf.name as farmer_name,
                   t.crop_listing_id, t.crop_name, t.quantity, t.price_per_unit, 
                   t.total_amount, t.transaction_date, t.status, t.notes
            FROM transactions t
            JOIN users uf ON t.farmer_id = uf.id
            WHERE t.buyer_id = ?
            ORDER BY t.transaction_date DESC
        ''', (buyer_id,))
        
        transactions = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': transaction[0],
                'buyer_id': transaction[1],
                'farmer_id': transaction[2],
                'farmer_name': transaction[3],
                'crop_listing_id': transaction[4],
                'crop_name': transaction[5],
                'quantity': transaction[6],
                'price_per_unit': transaction[7],
                'total_amount': transaction[8],
                'transaction_date': transaction[9],
                'status': transaction[10],
                'notes': transaction[11]
            }
            for transaction in transactions
        ]
