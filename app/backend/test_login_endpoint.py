#!/usr/bin/env python3
"""
Test script to verify the login endpoint works correctly
"""

import requests
import json
import sys

def test_login_endpoint():
    """Test the login endpoint"""
    
    # Test with local backend
    base_url = "http://localhost:5000"
    
    # Test data - using working credentials
    test_credentials = {
        "username_or_email": "testuser",
        "password": "TestPass123!"
    }
    
    print(f"🔐 Testing login endpoint at {base_url}/api/login")
    print(f"📝 Test credentials: {test_credentials['username_or_email']}")
    
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/api/login",
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            json=test_credentials,
            timeout=10
        )
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        # Try to get response data
        try:
            data = response.json()
            print(f"📄 Response data: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            print(f"❌ Response is not JSON: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login test successful!")
            return True
        else:
            print(f"❌ Login test failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the backend running?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timeout")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint"""
    
    base_url = "http://localhost:5000"
    
    print(f"🏥 Testing health endpoint at {base_url}/api/health")
    
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"📊 Health status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📄 Health data: {json.dumps(data, indent=2)}")
            print("✅ Health check successful!")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_db_endpoint():
    """Test the database endpoint"""
    
    base_url = "http://localhost:5000"
    
    print(f"🗄️ Testing database endpoint at {base_url}/api/db-test")
    
    try:
        response = requests.get(f"{base_url}/api/db-test", timeout=5)
        print(f"📊 DB test status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📄 DB test data: {json.dumps(data, indent=2)}")
            print("✅ Database test successful!")
            return True
        else:
            print(f"❌ Database test failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting backend endpoint tests...")
    print("=" * 50)
    
    # Test health endpoint first
    health_ok = test_health_endpoint()
    print()
    
    # Test database endpoint
    db_ok = test_db_endpoint()
    print()
    
    # Test login endpoint
    login_ok = test_login_endpoint()
    print()
    
    print("=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Database Test: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"   Login Test: {'✅ PASS' if login_ok else '❌ FAIL'}")
    
    if all([health_ok, db_ok, login_ok]):
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1) 