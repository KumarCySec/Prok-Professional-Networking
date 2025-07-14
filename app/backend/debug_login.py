#!/usr/bin/env python3
"""
Debug login endpoint to identify the specific error
"""

import os
import sys
import traceback
from flask import Flask, request, jsonify

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from extensions import db
from models.user import User

def debug_login():
    """Debug the login endpoint"""
    try:
        print("Setting up Flask app for debugging...")
        
        # Create Flask app
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            print("Testing database connection...")
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            
            # Test User model
            print("Testing User model...")
            try:
                user_count = User.query.count()
                print(f"✅ User model working. User count: {user_count}")
            except Exception as e:
                print(f"❌ User model error: {e}")
                traceback.print_exc()
                return False
            
            # Test user creation
            print("Testing user creation...")
            try:
                test_user = User(
                    username="debug_test",
                    email="debug@test.com",
                    password="DebugPass123!"
                )
                test_user.save()
                print("✅ Test user created successfully")
                
                # Test login logic
                print("Testing login logic...")
                user = User.find_by_username("debug_test")
                if user and user.check_password("DebugPass123!"):
                    print("✅ Login logic working")
                else:
                    print("❌ Login logic failed")
                
                # Clean up
                db.session.delete(test_user)
                db.session.commit()
                print("✅ Test user cleaned up")
                
            except Exception as e:
                print(f"❌ User creation/login test failed: {e}")
                traceback.print_exc()
                db.session.rollback()
                return False
            
            print("✅ All tests passed")
            return True
            
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_login()
    sys.exit(0 if success else 1) 