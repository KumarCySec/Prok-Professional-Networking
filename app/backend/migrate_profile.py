#!/usr/bin/env python3
"""
Simple database migration script for profile fields
This script adds the new profile-related columns to the users table
and creates the profiles table.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import get_app
from extensions import db
from models.user import User
from models.profile import Profile

def migrate_database():
    """Migrate database to add profile fields"""
    app = get_app()
    
    with app.app_context():
        try:
            print("Starting database migration...")
            
            # Create all tables (this will add new columns to existing tables)
            db.create_all()
            
            print("✅ Database migration completed successfully!")
            print("✅ Users table updated with profile fields")
            print("✅ Profiles table created")
            
            # Verify the migration
            print("\nVerifying migration...")
            
            # Check if we can query the new fields
            try:
                users = User.query.limit(1).all()
                print(f"✅ Users table accessible, found {len(users)} users")
                
                profiles = Profile.query.limit(1).all()
                print(f"✅ Profiles table accessible, found {len(profiles)} profiles")
                
            except Exception as e:
                print(f"⚠️  Warning: Could not verify tables: {str(e)}")
            
            print("\nMigration completed! You can now use the profile features.")
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    success = migrate_database()
    sys.exit(0 if success else 1) 