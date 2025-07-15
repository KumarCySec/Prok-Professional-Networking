#!/usr/bin/env python3
"""
Database initialization script for production deployment
Uses Flask-Migrate to ensure proper database schema
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

def init_database():
    """Initialize database with migrations"""
    try:
        print("🚀 Starting database initialization...")
        
        # Import after path setup
        from config import Config
        from extensions import db, migrate
        from models.user import User
        
        app = Flask(__name__)
        app.config.from_object(Config)
        
        print(f"📊 Database URL: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
        
        # Initialize extensions
        db.init_app(app)
        migrate.init_app(app, db)
        
        with app.app_context():
            print("🗄️ Running database migrations...")
            
            # Import Flask-Migrate commands
            from flask_migrate import upgrade, current
            
            # Check current migration status
            try:
                current_revision = current()
                print(f"📋 Current migration revision: {current_revision}")
            except Exception as e:
                print(f"⚠️ Could not get current revision (this is normal for new databases): {e}")
            
            # Run migrations
            upgrade()
            print("✅ Database migrations completed successfully")
            
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
                    print("📝 Sample user credentials:")
                    print("   Username: testuser")
                    print("   Email: test@example.com")
                    print("   Password: Test123!")
                except Exception as e:
                    print(f"⚠️ Sample user creation failed (this is okay): {e}")
            
            print("✅ Database initialization completed successfully")
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("🔍 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1) 