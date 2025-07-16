#!/usr/bin/env python3
"""
Deployment Verification Script
This script helps verify if the deployment is configured correctly
"""

import requests
import json

def test_backend_endpoints():
    """Test backend endpoints to verify deployment"""
    base_url = "https://prok-professional-networking-dvec.onrender.com"
    
    print("🧪 Testing Backend Endpoints")
    print("="*40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
    
    # Test debug config endpoint
    try:
        response = requests.get(f"{base_url}/api/debug-config")
        if response.status_code == 200:
            config = response.json()
            print(f"✅ Debug Config: {response.status_code}")
            print(f"   DATABASE_URL set: {config.get('database_url_set')}")
            print(f"   Using PostgreSQL: {config.get('is_postgresql')}")
            print(f"   Using SQLite: {config.get('is_sqlite')}")
            print(f"   Database URL: {config.get('database_url_preview')}")
        else:
            print(f"❌ Debug Config: {response.status_code}")
    except Exception as e:
        print(f"❌ Debug Config Failed: {e}")
    
    # Test database endpoint
    try:
        response = requests.get(f"{base_url}/api/db-test")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Database Test: {response.status_code} - {result.get('message')}")
            print(f"   User count: {result.get('user_count', 'N/A')}")
        else:
            result = response.json()
            print(f"❌ Database Test: {response.status_code} - {result.get('message')}")
            print(f"   Error: {result.get('error', 'No error details')[:100]}...")
    except Exception as e:
        print(f"❌ Database Test Failed: {e}")

def provide_fix_instructions():
    """Provide fix instructions based on test results"""
    print("\n" + "="*60)
    print("🔧 DEPLOYMENT FIX INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ VERIFY ENVIRONMENT VARIABLES:")
    print("   • Go to https://dashboard.render.com")
    print("   • Open your backend service: prok-professional-networking-dvec")
    print("   • Click 'Environment' tab")
    print("   • Verify these variables are set:")
    print("     DATABASE_URL = postgresql://prok_database_texr_user:UJ5uuxzIGYa37uWxoiDP3k1CacPQwKX3@dpg-d1rq0mvgi27c73cm8drg-a.oregon-postgres.render.com/prok_database_texr")
    print("     SECRET_KEY = my-super-secret-key-change-this-in-production-12345")
    print("     JWT_SECRET_KEY = jwt-super-secret-key-change-this-in-production-67890")
    print("     ALLOWED_ORIGINS = https://prok-professional-networking-dvec.onrender.com,https://prok-frontend-4h1s.onrender.com,http://localhost:5173")
    
    print("\n2️⃣ FORCE REDEPLOY:")
    print("   • Click 'Save Changes' (even if no changes)")
    print("   • Go to 'Manual Deploy' tab")
    print("   • Click 'Deploy latest commit'")
    print("   • Wait 2-3 minutes for deployment")
    
    print("\n3️⃣ CHECK DEPLOYMENT LOGS:")
    print("   • Go to 'Logs' tab in your backend service")
    print("   • Look for database initialization messages")
    print("   • Check for any error messages")
    
    print("\n4️⃣ TEST AGAIN:")
    print("   • Run this script again after deployment")
    print("   • Check if database test returns success")

def main():
    print("🚀 Backend Deployment Verification")
    print("="*50)
    
    # Test endpoints
    test_backend_endpoints()
    
    # Provide instructions
    provide_fix_instructions()
    
    print("\n" + "="*60)
    print("📞 Need help? Check Render deployment logs")
    print("="*60)

if __name__ == "__main__":
    main() 