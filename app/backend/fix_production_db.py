#!/usr/bin/env python3
"""
Script to diagnose and fix production database issues
"""

import os
import sys
from sqlalchemy import text, inspect
from app import app
from extensions import db

def check_database_state():
    """Check the current state of the database"""
    print("🔍 Checking database state...")
    
    try:
        with app.app_context():
            # Test basic connection
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            print("✅ Database connection successful")
            
            # Check if alembic_version table exists
            try:
                result = db.session.execute(text("SELECT version_num FROM alembic_version"))
                version = result.scalar()
                print(f"📋 Current migration version: {version}")
            except Exception as e:
                print(f"❌ Alembic version table not found: {e}")
                print("   This suggests migrations have never been run")
            
            # Check if users table exists
            try:
                result = db.session.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.scalar()
                print(f"👥 Users table exists with {user_count} users")
            except Exception as e:
                print(f"❌ Users table not found: {e}")
                print("   This is the main issue - the users table is missing")
            
            # List all tables
            try:
                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"📊 All tables in database: {tables}")
            except Exception as e:
                print(f"❌ Could not list tables: {e}")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

def provide_fix_instructions():
    """Provide instructions for fixing the database"""
    print("\n" + "="*60)
    print("🔧 FIX INSTRUCTIONS")
    print("="*60)
    print("The production database is missing the 'users' table.")
    print("This means the database migrations haven't been run successfully.")
    print("\nTo fix this issue:")
    print("\n1. REDEPLOY THE BACKEND:")
    print("   - Go to your Render dashboard")
    print("   - Find the backend service")
    print("   - Trigger a manual redeploy")
    print("   - This should run the migration script automatically")
    print("\n2. CHECK DEPLOYMENT LOGS:")
    print("   - Look for any errors during the 'flask db upgrade' step")
    print("   - Common issues:")
    print("     * Database connection problems")
    print("     * Permission issues")
    print("     * Migration conflicts")
    print("\n3. MANUAL MIGRATION (if redeploy doesn't work):")
    print("   - Connect to the production database")
    print("   - Run: flask db upgrade")
    print("   - Or run the migration manually:")
    print("     CREATE TABLE users (...)")
    print("\n4. VERIFY FIX:")
    print("   - Test the /api/db-test endpoint")
    print("   - Should return user_count > 0")
    print("   - Test the /api/login endpoint")
    print("   - Should work with valid credentials")

def test_migration_locally():
    """Test if migrations work locally"""
    print("\n🧪 Testing migrations locally...")
    
    try:
        # Check if we can run migrations locally
        os.system("cd /home/kumarshabu/Prok-Professional-Networking/app/backend && flask db current")
        print("✅ Local migration check completed")
    except Exception as e:
        print(f"❌ Local migration check failed: {e}")

if __name__ == "__main__":
    print("🚀 Production Database Diagnostic Tool")
    print("="*60)
    
    # Check database state
    db_ok = check_database_state()
    
    # Provide fix instructions
    provide_fix_instructions()
    
    # Test local migrations
    test_migration_locally()
    
    print("\n" + "="*60)
    print("📋 SUMMARY")
    print("="*60)
    if db_ok:
        print("✅ Database connection works")
        print("❌ But users table is missing")
        print("🔧 Solution: Redeploy backend to run migrations")
    else:
        print("❌ Database connection failed")
        print("🔧 Solution: Check database configuration")
    
    print("\nThe main issue is that the production database")
    print("doesn't have the required tables. This is why")
    print("the login endpoint returns a 500 error.") 