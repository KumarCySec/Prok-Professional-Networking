#!/usr/bin/env python3
"""
Database Debug Script
This script helps identify and fix database configuration issues
"""

import os
import sys

def check_environment():
    """Check environment variables and configuration"""
    print("🔍 Checking environment configuration...")
    
    # Check DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL is set: {database_url[:50]}...")
        if database_url.startswith('postgresql://'):
            print("✅ Using PostgreSQL database")
        elif database_url.startswith('postgres://'):
            print("⚠️ Using old postgres:// format (should be postgresql://)")
        elif database_url.startswith('sqlite://'):
            print("❌ Still using SQLite - this won't work on Render!")
        else:
            print(f"❓ Unknown database format: {database_url[:20]}...")
    else:
        print("❌ DATABASE_URL is NOT set!")
        print("   This is why you're getting database errors.")
    
    # Check other required variables
    secret_key = os.environ.get('SECRET_KEY')
    jwt_secret = os.environ.get('JWT_SECRET_KEY')
    
    print(f"SECRET_KEY: {'✅ Set' if secret_key else '❌ Not set'}")
    print(f"JWT_SECRET_KEY: {'✅ Set' if jwt_secret else '❌ Not set'}")
    
    return database_url is not None and database_url.startswith('postgres')

def provide_fix_instructions():
    """Provide step-by-step fix instructions"""
    print("\n" + "="*60)
    print("🔧 FIX INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ CREATE POSTGRESQL DATABASE:")
    print("   • Go to https://dashboard.render.com")
    print("   • Click 'New' → 'PostgreSQL'")
    print("   • Name: prok-database")
    print("   • Plan: Free")
    print("   • Click 'Create Database'")
    
    print("\n2️⃣ GET DATABASE URL:")
    print("   • Click on your new PostgreSQL database")
    print("   • Copy the 'External Database URL'")
    print("   • It should look like: postgresql://user:pass@host:port/dbname")
    
    print("\n3️⃣ UPDATE BACKEND ENVIRONMENT VARIABLES:")
    print("   • Go to your backend service (prok-professional-networking-dvec)")
    print("   • Click 'Environment' tab")
    print("   • Add/Update these variables:")
    print("     DATABASE_URL = [Paste the PostgreSQL URL]")
    print("     SECRET_KEY = my-secret-key-12345")
    print("     JWT_SECRET_KEY = jwt-secret-key-67890")
    print("     ALLOWED_ORIGINS = https://prok-professional-networking-dvec.onrender.com,https://prok-frontend-4h1s.onrender.com,http://localhost:5173")
    
    print("\n4️⃣ REDEPLOY:")
    print("   • Click 'Save Changes'")
    print("   • Go to 'Manual Deploy' tab")
    print("   • Click 'Deploy latest commit'")
    
    print("\n5️⃣ TEST:")
    print("   • Wait for deployment to complete")
    print("   • Test: curl https://prok-professional-networking-dvec.onrender.com/api/db-test")
    print("   • Should return success, not SQLite error")

def main():
    print("🚀 Database Configuration Debug Tool")
    print("="*40)
    
    # Check current configuration
    is_configured = check_environment()
    
    if not is_configured:
        provide_fix_instructions()
    else:
        print("\n✅ Database appears to be configured correctly!")
        print("   If you're still getting errors, check the deployment logs.")
    
    print("\n" + "="*60)
    print("📞 Need help? Check the deployment logs in Render dashboard")
    print("="*60)

if __name__ == "__main__":
    main() 