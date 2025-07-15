#!/usr/bin/env python3
"""
Test script to verify deployment fixes are working correctly
Run this after deployment to ensure everything is functioning
"""

import os
import sys
import requests
import json
import time
from urllib.parse import urljoin

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_endpoint(base_url, endpoint, method='GET', data=None, headers=None, expected_status=200):
    """Test a specific endpoint"""
    url = urljoin(base_url, endpoint)
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
            
        print(f"🔍 Testing {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"   ✅ PASSED (Expected {expected_status})")
            if response.content:
                try:
                    result = response.json()
                    if 'error' in result:
                        print(f"   📝 Response: {result['error']}")
                    else:
                        print(f"   📝 Response: {list(result.keys())}")
                except:
                    print(f"   📝 Response: {response.text[:100]}...")
        else:
            print(f"   ❌ FAILED (Expected {expected_status}, got {response.status_code})")
            if response.content:
                try:
                    result = response.json()
                    print(f"   📝 Error: {result}")
                except:
                    print(f"   📝 Error: {response.text[:100]}...")
            return False
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ REQUEST ERROR: {e}")
        return False
    except Exception as e:
        print(f"   ❌ UNEXPECTED ERROR: {e}")
        return False

def test_deployment_fixes():
    """Test all deployment fixes"""
    print("🚀 Testing Deployment Fixes")
    print("=" * 50)
    
    # Get base URL from environment or use default
    base_url = os.getenv('TEST_BASE_URL', 'https://prok-professional-networking-1-iv6a.onrender.com')
    print(f"📍 Testing against: {base_url}")
    print()
    
    # Test results tracking
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Check")
    if test_endpoint(base_url, '/api/health'):
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 2: Database Connection
    print("2️⃣ Testing Database Connection")
    if test_endpoint(base_url, '/api/db-test'):
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 3: CORS Test
    print("3️⃣ Testing CORS Configuration")
    if test_endpoint(base_url, '/api/cors-test'):
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 4: Login with Invalid Credentials (should return 401, not 500)
    print("4️⃣ Testing Login Error Handling")
    login_data = {
        "username_or_email": "nonexistent",
        "password": "wrongpassword"
    }
    if test_endpoint(base_url, '/api/login', method='POST', data=login_data, expected_status=401):
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 5: Login with Valid Test User
    print("5️⃣ Testing Login with Test User")
    test_login_data = {
        "username_or_email": "testuser",
        "password": "Test123!"
    }
    if test_endpoint(base_url, '/api/login', method='POST', data=test_login_data, expected_status=200):
        tests_passed += 1
        print("   💡 Test user login successful - you can use these credentials:")
        print("      Username: testuser")
        print("      Password: Test123!")
    else:
        tests_failed += 1
    print()
    
    # Test 6: Login with Email
    print("6️⃣ Testing Login with Email")
    email_login_data = {
        "username_or_email": "test@example.com",
        "password": "Test123!"
    }
    if test_endpoint(base_url, '/api/login', method='POST', data=email_login_data, expected_status=200):
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 7: Missing Data Handling
    print("7️⃣ Testing Missing Data Handling")
    empty_data = {}
    if test_endpoint(base_url, '/api/login', method='POST', data=empty_data, expected_status=400):
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 8: Invalid JSON Handling
    print("8️⃣ Testing Invalid JSON Handling")
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(
            urljoin(base_url, '/api/login'),
            data="invalid json",
            headers=headers,
            timeout=10
        )
        if response.status_code in [400, 500]:  # Either is acceptable for invalid JSON
            print("   ✅ PASSED (Handled invalid JSON)")
            tests_passed += 1
        else:
            print(f"   ❌ FAILED (Unexpected status: {response.status_code})")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ REQUEST ERROR: {e}")
        tests_failed += 1
    print()
    
    # Summary
    print("=" * 50)
    print("📊 TEST SUMMARY")
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📈 Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
    
    if tests_failed == 0:
        print("🎉 ALL TESTS PASSED! Deployment fixes are working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the deployment and try again.")
        return False

def test_local_setup():
    """Test local setup for development"""
    print("🔧 Testing Local Setup")
    print("=" * 30)
    
    try:
        from config import Config
        from extensions import db, migrate
        from models.user import User
        
        print("✅ Config imported successfully")
        print("✅ Extensions imported successfully")
        print("✅ User model imported successfully")
        
        # Test Flask app creation
        from flask import Flask
        app = Flask(__name__)
        app.config.from_object(Config)
        
        db.init_app(app)
        migrate.init_app(app, db)
        
        with app.app_context():
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ Database connection working")
            
            # Test User model
            user_count = User.query.count()
            print(f"✅ User model working. User count: {user_count}")
        
        print("✅ Local setup is working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Local setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test deployment fixes')
    parser.add_argument('--local', action='store_true', help='Test local setup only')
    parser.add_argument('--url', type=str, help='Base URL for testing (default: production)')
    
    args = parser.parse_args()
    
    if args.url:
        os.environ['TEST_BASE_URL'] = args.url
    
    if args.local:
        success = test_local_setup()
    else:
        success = test_deployment_fixes()
    
    sys.exit(0 if success else 1) 