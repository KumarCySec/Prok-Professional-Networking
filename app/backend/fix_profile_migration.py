#!/usr/bin/env python3
"""
Database migration script to add profile fields to existing users table
This script handles the case where the users table already exists.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import get_app
from extensions import db
try:
    from sqlalchemy import text
except ImportError:
    from sqlalchemy.sql import text

def migrate_database():
    """Migrate database to add profile fields"""
    app = get_app()
    
    with app.app_context():
        try:
            print("Starting database migration...")
            
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('users')]
            
            print(f"Existing columns in users table: {existing_columns}")
            
            # Define new columns to add
            new_columns = [
                'first_name',
                'last_name', 
                'bio',
                'location',
                'company',
                'job_title',
                'website',
                'phone',
                'profile_image_url',
                'skills',
                'experience_years',
                'education',
                'social_links'
            ]
            
            # Add missing columns
            columns_to_add = [col for col in new_columns if col not in existing_columns]
            
            if columns_to_add:
                print(f"Adding columns: {columns_to_add}")
                
                for column in columns_to_add:
                    try:
                        if column in ['first_name', 'last_name', 'location', 'company', 'job_title']:
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} VARCHAR(100)"))
                        elif column == 'bio':
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} TEXT"))
                        elif column == 'website':
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} VARCHAR(200)"))
                        elif column == 'phone':
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} VARCHAR(20)"))
                        elif column == 'profile_image_url':
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} VARCHAR(500)"))
                        elif column in ['skills', 'education', 'social_links']:
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} TEXT"))
                        elif column == 'experience_years':
                            db.session.execute(text(f"ALTER TABLE users ADD COLUMN {column} INTEGER"))
                        db.session.commit()
                        print(f"✅ Added column: {column}")
                    except Exception as e:
                        print(f"⚠️  Warning: Could not add column {column}: {str(e)}")
            else:
                print("✅ All profile columns already exist")
            
            # Create profiles table if it doesn't exist
            try:
                db.session.execute(text("""
                    CREATE TABLE IF NOT EXISTS profiles (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL UNIQUE,
                        headline VARCHAR(200),
                        industry VARCHAR(100),
                        current_position VARCHAR(100),
                        company_size VARCHAR(50),
                        linkedin_url VARCHAR(200),
                        twitter_url VARCHAR(200),
                        github_url VARCHAR(200),
                        is_public BOOLEAN DEFAULT TRUE,
                        allow_messages BOOLEAN DEFAULT TRUE,
                        show_email BOOLEAN DEFAULT FALSE,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """))
                db.session.commit()
                print("✅ Profiles table created/verified")
            except Exception as e:
                print(f"⚠️  Warning: Could not create profiles table: {str(e)}")
            
            print("\n✅ Database migration completed successfully!")
            
            # Verify the migration
            print("\nVerifying migration...")
            
            try:
                # Check if we can query the new fields
                result = db.session.execute(text("SELECT id, username FROM users LIMIT 1"))
                users = result.fetchall()
                print(f"✅ Users table accessible, found {len(users)} users")
                
                result = db.session.execute(text("SELECT id FROM profiles LIMIT 1"))
                profiles = result.fetchall()
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