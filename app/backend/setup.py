#!/usr/bin/env python3
"""
Quick setup script for production
"""

import os
import sys
import logging
import traceback
from flask import Flask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_setup():
    """Quick database setup"""
    try:
        print("🚀 Starting quick database setup...")
        
        # Import after path setup
        from config import Config
        from extensions import db
        from models.user import User
        
        app = Flask(__name__)
        app.config.from_object(Config)
        
        print(f"📊 Database URL: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
        
        db.init_app(app)
        
        with app.app_context():
            print("🗄️ Creating tables...")
            db.create_all()
            print("✅ Tables created successfully")
            
            # Test connection
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection working")
            
            # Test User model
            user_count = User.query.count()
            print(f"✅ User model working. User count: {user_count}")
            
            # Test creating a sample user if none exist
            if user_count == 0:
                print("👤 Creating sample user for testing...")
                try:
                    sample_user = User(
                        username="testuser",
                        email="test@example.com",
                        password="Test123!"
                    )
                    sample_user.save()
                    print("✅ Sample user created successfully")
                except Exception as e:
                   print(f"⚠️ Sample user creation failed (this is okay): {e}")
            
            print("✅ Quick setup completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Quick setup failed: {e}")
        print("🔍 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_setup()
    sys.exit(0 if success else 1) 