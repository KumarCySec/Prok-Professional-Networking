#!/usr/bin/env python3
"""
Initialize database and run migrations
This script should be run on the production server to set up the database
"""

import os
import sys
from flask import Flask

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from extensions import db, migrate
from models.user import User
from models.profile import Profile
from models.post import Post

def init_database():
    """Initialize database and run migrations"""
    try:
        print("Initializing database...")
        
        # Create Flask app
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # Initialize extensions
        db.init_app(app)
        migrate.init_app(app, db)
        
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Run migrations if needed
            try:
                from flask_migrate import upgrade
                print("Running migrations...")
                upgrade()
                print("✅ Migrations completed successfully")
            except Exception as e:
                print(f"⚠️ Migration warning: {e}")
            
            # Test database connection
            print("Testing database connection...")
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection test successful")
            
            # Check if users table exists and has data
            user_count = User.query.count()
            print(f"✅ Users table exists with {user_count} users")
            
            print("✅ Database initialization completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1) 