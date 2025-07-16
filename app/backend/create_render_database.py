#!/usr/bin/env python3
"""
Database setup script for Render deployment
This script creates all necessary tables and initial data for the Prok application
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.user import User
from models.profile import Profile
from models.post import Post

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Set up the database with all tables and initial data"""
    try:
        app = create_app()
        
        with app.app_context():
            logger.info("🔧 Starting database setup...")
            
            # Create all tables
            logger.info("📋 Creating database tables...")
            db.create_all()
            logger.info("✅ All tables created successfully")
            
            # Create indexes for better performance
            logger.info("📊 Creating database indexes...")
            create_indexes()
            logger.info("✅ Indexes created successfully")
            
            # Insert initial data if needed
            logger.info("📝 Checking for initial data...")
            insert_initial_data()
            logger.info("✅ Initial data setup completed")
            
            logger.info("🎉 Database setup completed successfully!")
            
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        raise

def create_indexes():
    """Create database indexes for better performance"""
    try:
        # User indexes
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
        """))
        
        # Profile indexes
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
            CREATE INDEX IF NOT EXISTS idx_profiles_location ON profiles(location);
            CREATE INDEX IF NOT EXISTS idx_profiles_industry ON profiles(industry);
        """))
        
        # Post indexes
        db.session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
            CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);
            CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category);
            CREATE INDEX IF NOT EXISTS idx_posts_content_search ON posts USING gin(to_tsvector('english', content));
        """))
        
        # Note: Job and Message indexes will be added when those models are implemented
        
        db.session.commit()
        
    except SQLAlchemyError as e:
        logger.warning(f"⚠️ Some indexes may already exist: {e}")
        db.session.rollback()

def insert_initial_data():
    """Insert initial data if the database is empty"""
    try:
        # Check if we have any users
        user_count = User.query.count()
        
        if user_count == 0:
            logger.info("👤 Creating sample admin user...")
            
            # Create a sample admin user
            admin_user = User(
                username='admin',
                email='admin@prok.com',
                password='Admin@123'
            )
            admin_user.save()
            
            # Create admin profile
            admin_profile = Profile(
                user_id=admin_user.id,
                first_name='Admin',
                last_name='User',
                headline='System Administrator',
                location='Remote',
                industry='Technology',
                about='System administrator for Prok Professional Networking platform.',
                skills=['Python', 'Flask', 'PostgreSQL', 'System Administration']
            )
            db.session.add(admin_profile)
            db.session.commit()
            
            logger.info("✅ Sample admin user created")
        else:
            logger.info(f"📊 Database already contains {user_count} users")
            
    except Exception as e:
        logger.warning(f"⚠️ Could not create initial data: {e}")
        db.session.rollback()

def test_database_connection():
    """Test the database connection"""
    try:
        app = create_app()
        
        with app.app_context():
            # Test basic connection
            result = db.session.execute(text('SELECT 1'))
            logger.info("✅ Database connection test successful")
            
            # Test table access
            tables = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)).fetchall()
            
            logger.info(f"📋 Available tables: {[table[0] for table in tables]}")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {e}")
        return False

if __name__ == '__main__':
    try:
        # Test connection first
        if test_database_connection():
            # Setup database
            setup_database()
            print("🎉 Database deployment completed successfully!")
        else:
            print("❌ Database connection failed. Please check your configuration.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Database deployment failed: {e}")
        sys.exit(1) 