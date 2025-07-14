#!/usr/bin/env python3
"""
Test database connection and create tables if needed
"""

import os
import sys
from sqlalchemy import text
from urllib.parse import quote_plus

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from extensions import db
from models.user import User

def test_database_connection():
    """Test database connection and create tables"""
    try:
        print("Testing database connection...")
        
        # Create Flask app context
        from flask import Flask
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            # Test basic connection
            print("Testing basic connection...")
            result = db.session.execute(text('SELECT 1'))
            print("✅ Basic connection successful")
            
            # Check if users table exists
            print("Checking if users table exists...")
            result = db.session.execute(text("SHOW TABLES LIKE 'users'"))
            tables = result.fetchall()
            
            if not tables:
                print("❌ Users table does not exist. Creating tables...")
                db.create_all()
                print("✅ Tables created successfully")
            else:
                print("✅ Users table exists")
            
            # Test User model
            print("Testing User model...")
            user_count = User.query.count()
            print(f"✅ User model working. Current user count: {user_count}")
            
            # Test creating a test user
            print("Testing user creation...")
            try:
                test_user = User(
                    username="test_user",
                    email="test@example.com",
                    password="TestPass123!"
                )
                test_user.save()
                print("✅ Test user created successfully")
                
                # Clean up test user
                db.session.delete(test_user)
                db.session.commit()
                print("✅ Test user cleaned up")
                
            except Exception as e:
                print(f"⚠️ Test user creation failed: {e}")
                db.session.rollback()
            
            print("✅ Database connection test completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1) 