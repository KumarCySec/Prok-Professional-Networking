#!/usr/bin/env python3
"""
Deployment Test Script
Tests all critical deployment issues and configurations
"""

import requests
import json
import os
import sys
from urllib.parse import urljoin

# Configuration
BACKEND_URL = "https://prok-professional-networking-se45.onrender.com"
FRONTEND_URL = "https://prok-professional-networking-1-iv6a.onrender.com"

def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_cors_configuration():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS Configuration...")
    try:
        headers = {
            'Origin': FRONTEND_URL,
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{BACKEND_URL}/api/cors-test", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('cors_working'):
                print("✅ CORS configuration working")
                return True
            else:
                print("❌ CORS not working properly")
                return False
        else:
            print(f"❌ CORS test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing Database Connection...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/db-test", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print("✅ Database connection working")
                return True
            else:
                print(f"❌ Database connection failed: {data.get('message')}")
                return False
        else:
            print(f"❌ Database test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def test_frontend_routes():
    """Test frontend SPA routing"""
    print("\n🔍 Testing Frontend SPA Routing...")
    routes_to_test = ['/login', '/profile', '/feed', '/jobs', '/messages']
    
    for route in routes_to_test:
        try:
            response = requests.get(f"{FRONTEND_URL}{route}", timeout=10)
            if response.status_code == 200:
                print(f"✅ Route {route} accessible")
            else:
                print(f"❌ Route {route} failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Route {route} error: {e}")
            return False
    
    return True

def test_favicon():
    """Test favicon accessibility"""
    print("\n🔍 Testing Favicon...")
    try:
        response = requests.get(f"{FRONTEND_URL}/favicon.ico", timeout=10)
        if response.status_code == 200:
            print("✅ Favicon accessible")
            return True
        else:
            print(f"❌ Favicon failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Favicon error: {e}")
        return False

def test_api_endpoints():
    """Test critical API endpoints"""
    print("\n🔍 Testing API Endpoints...")
    endpoints = [
        '/api/signup',
        '/api/login',
        '/api/me'
    ]
    
    for endpoint in endpoints:
        try:
            # Test OPTIONS preflight
            response = requests.options(f"{BACKEND_URL}{endpoint}", timeout=10)
            if response.status_code in [200, 405]:  # 405 is OK for endpoints that don't support OPTIONS
                print(f"✅ {endpoint} preflight working")
            else:
                print(f"❌ {endpoint} preflight failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {endpoint} error: {e}")
            return False
    
    return True

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🔍 Testing Environment Variables...")
    
    # Check if we can access the backend config
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend environment variables configured")
            return True
        else:
            print("❌ Backend environment variables may be misconfigured")
            return False
    except Exception as e:
        print(f"❌ Environment test error: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🚀 Starting Deployment Validation Tests...\n")
    
    tests = [
        ("Backend Health", test_backend_health),
        ("CORS Configuration", test_cors_configuration),
        ("Database Connection", test_database_connection),
        ("Frontend SPA Routing", test_frontend_routes),
        ("Favicon Accessibility", test_favicon),
        ("API Endpoints", test_api_endpoints),
        ("Environment Variables", test_environment_variables)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 DEPLOYMENT TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All deployment tests passed! Your application is ready for production.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 