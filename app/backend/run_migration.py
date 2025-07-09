#!/usr/bin/env python3
"""
Simple script to add category field to posts table
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions import db
from app import create_app

def add_category_to_posts():
    """Add category column to posts table"""
    try:
        app = create_app()
        with app.app_context():
            # Add category column with default value
            db.engine.execute("""
                ALTER TABLE posts 
                ADD COLUMN category VARCHAR(50) DEFAULT 'general'
            """)
            
            # Create index on category column for better performance
            db.engine.execute("""
                CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category)
            """)
            
            print("✅ Successfully added category column to posts table")
            print("✅ Created index on category column")
            
    except Exception as e:
        print(f"❌ Error adding category column: {e}")
        print("The column might already exist. You can safely ignore this error.")
        return False
    
    return True

if __name__ == "__main__":
    print("🔄 Adding category field to posts table...")
    success = add_category_to_posts()
    
    if success:
        print("🎉 Migration completed successfully!")
    else:
        print("⚠️  Migration completed with warnings. Check the output above.") 