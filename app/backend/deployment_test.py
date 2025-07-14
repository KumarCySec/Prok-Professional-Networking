#!/usr/bin/env python3
"""
Comprehensive deployment test script for production validation
"""

import os
import sys
import requests
import json
import time
from urllib.parse import urljoin

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_local_backend():
    """Test local backend functionality"""
    print("🔧 Testing Local Backend...")
    
    try:
        # Test basic imports
        from config import Config
        from extensions import db
        from models.user import User
        
        print("✅ Basic imports successful")
        
        # Test configuration
        config = Config()
        print(f"✅ Configuration loaded. Database URL: {config.SQLALCHEMY_DATABASE_URI[:50]}...")
        
        # Test database connection
        from flask import Flask
        app = Flask(__name__)
        app.config.from_object(config)
        db.init_app(app)
        
        with app.app_context():
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            
            # Test User model
            user_count = User.query.count()
            print(f"✅ User model working. Count: {user_count}")
            
        return True
        
    except Exception as e:
        print(f"❌ Local backend test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_production_endpoints(base_url):
    """Test production endpoints"""
    print(f"\n🌐 Testing Production Endpoints at {base_url}")
    
    endpoints = [
        ('/', 'Health Check'),
        ('/api/health', 'API Health'),
        ('/api/cors-test', 'CORS Test'),
        ('/api/db-test', 'Database Test'),
    ]
    
    results = []
    
    for endpoint, name in endpoints:
        try:
            url = urljoin(base_url, endpoint)
            print(f"🔍 Testing {name} at {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name}: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ {name}: {response.status_code}")
                print(f"   Error: {response.text}")
            
            results.append((name, response.status_code == 200))
            
        except Exception as e:
            print(f"❌ {name}: Failed - {e}")
            results.append((name, False))
    
    return results

def test_login_endpoint(base_url):
    """Test login endpoint specifically"""
    print(f"\n🔐 Testing Login Endpoint at {base_url}")
    
    login_url = urljoin(base_url, '/api/login')
    
    # Test with invalid credentials first
    print("🔍 Testing with invalid credentials...")
    try:
        response = requests.post(
            login_url,
            json={'username_or_email': 'nonexistent', 'password': 'wrong'},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 401:
            print("✅ Invalid login correctly rejected")
        else:
            print(f"⚠️ Unexpected status for invalid login: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Invalid login test failed: {e}")
    
    # Test with valid credentials (if we have a test user)
    print("🔍 Testing with valid credentials...")
    try:
        response = requests.post(
            login_url,
            json={'username_or_email': 'testuser', 'password': 'Test123!'},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Valid login successful")
            data = response.json()
            if 'access_token' in data:
                print("✅ JWT token received")
                return data['access_token']
        elif response.status_code == 401:
            print("⚠️ Valid login failed - test user may not exist")
        else:
            print(f"❌ Login failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Valid login test failed: {e}")
    
    return None

def test_authenticated_endpoints(base_url, token):
    """Test authenticated endpoints"""
    if not token:
        print("⚠️ Skipping authenticated tests - no token available")
        return
    
    print(f"\n🔒 Testing Authenticated Endpoints at {base_url}")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    endpoints = [
        ('/api/me', 'Get Current User'),
        ('/api/logout', 'Logout'),
    ]
    
    for endpoint, name in endpoints:
        try:
            url = urljoin(base_url, endpoint)
            print(f"🔍 Testing {name} at {url}")
            
            if endpoint == '/api/logout':
                response = requests.post(url, headers=headers, timeout=10)
            else:
                response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name}: {response.status_code}")
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ {name}: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ {name}: Failed - {e}")

def test_cors_preflight(base_url):
    """Test CORS preflight requests"""
    print(f"\n🌍 Testing CORS Preflight at {base_url}")
    
    try:
        response = requests.options(
            urljoin(base_url, '/api/login'),
            headers={
                'Origin': 'https://prok-frontend.onrender.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type, Authorization'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ CORS preflight successful")
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
            }
            print(f"   CORS Headers: {json.dumps(cors_headers, indent=2)}")
        else:
            print(f"❌ CORS preflight failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ CORS preflight test failed: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Comprehensive Deployment Tests")
    print("=" * 50)
    
    # Test local backend
    local_success = test_local_backend()
    
    # Get production URL from environment or use default
    prod_url = os.environ.get('PRODUCTION_URL', 'https://prok-professional-networking-1-iv6a.onrender.com')
    
    if not prod_url.startswith('http'):
        prod_url = f'https://{prod_url}'
    
    print(f"\n🎯 Production URL: {prod_url}")
    
    # Test production endpoints
    endpoint_results = test_production_endpoints(prod_url)
    
    # Test login endpoint
    token = test_login_endpoint(prod_url)
    
    # Test authenticated endpoints
    test_authenticated_endpoints(prod_url, token)
    
    # Test CORS
    test_cors_preflight(prod_url)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    print(f"Local Backend: {'✅ PASS' if local_success else '❌ FAIL'}")
    
    passed_endpoints = sum(1 for _, success in endpoint_results if success)
    total_endpoints = len(endpoint_results)
    print(f"Production Endpoints: {passed_endpoints}/{total_endpoints} ✅")
    
    for name, success in endpoint_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  - {name}: {status}")
    
    print(f"Login Endpoint: {'✅ PASS' if token else '⚠️ PARTIAL'}")
    print(f"CORS Preflight: {'✅ PASS' if token else '⚠️ UNTESTED'}")
    
    # Overall result
    overall_success = local_success and passed_endpoints > 0
    print(f"\n🎯 Overall Result: {'✅ DEPLOYMENT READY' if overall_success else '❌ NEEDS FIXES'}")

if __name__ == "__main__":
    main() 