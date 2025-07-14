#!/usr/bin/env python3
"""
Quick setup script for production
"""

import os
import sys
from flask import Flask

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from extensions import db
from models.user import User

def quick_setup():
    """Quick database setup"""
    try:
        print("Starting quick database setup...")
        
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)
        
        with app.app_context():
            print("Creating tables...")
            db.create_all()
            print("✅ Tables created")
            
            # Test connection
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection working")
            
            # Test User model
            user_count = User.query.count()
            print(f"✅ User model working. User count: {user_count}")
            
            print("✅ Quick setup completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Quick setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_setup()
    sys.exit(0 if success else 1) 