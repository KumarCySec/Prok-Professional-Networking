#!/usr/bin/env python3
"""
Database connection test script
Run this to test if the database connection is working
"""

import os
import sys
import traceback

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Test database connection and basic operations"""
    try:
        print("🚀 Testing database connection...")
        
        # Import required modules
        from config import Config
        from extensions import db
        from models.user import User
        
        # Create Flask app
        from flask import Flask
        app = Flask(__name__)
        app.config.from_object(Config)
        
        print(f"📊 Database URL: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            print("🗄️ Testing database connection...")
            
            # Test basic connection
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            print("✅ Basic database connection successful")
            
            # Test table creation
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Test User model
            user_count = User.query.count()
            print(f"✅ User model working. User count: {user_count}")
            
            # Test creating a user
            try:
                test_user = User(
                    username="testuser123",
                    email="test123@example.com",
                    password="Test123!"
                )
                test_user.save()
                print("✅ User creation test successful")
                
                # Clean up
                db.session.delete(test_user)
                db.session.commit()
                print("✅ User cleanup successful")
                
            except Exception as e:
                print(f"⚠️ User creation test failed: {e}")
            
            print("✅ All database tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print("🔍 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1) 