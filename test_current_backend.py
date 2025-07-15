#!/usr/bin/env python3
"""
Test script to verify current backend state and test after deployment
"""

import requests
import json
import sys

def test_backend(url):
    """Test the current backend state"""
    print(f"🔍 Testing backend at: {url}")
    print("=" * 50)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Check")
    try:
        response = requests.get(f"{url}/api/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ PASSED")
            tests_passed += 1
        else:
            print("   ❌ FAILED")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        tests_failed += 1
    print()
    
    # Test 2: Database Test
    print("2️⃣ Testing Database Connection")
    try:
        response = requests.get(f"{url}/api/db-test", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ PASSED - Database working")
            tests_passed += 1
        elif response.status_code == 500:
            data = response.json()
            if "users" in data.get('error', ''):
                print("   ⚠️ FAILED - Users table missing (expected before fix)")
                tests_failed += 1
            else:
                print("   ❌ FAILED - Other database error")
                tests_failed += 1
        else:
            print("   ❌ FAILED")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        tests_failed += 1
    print()
    
    # Test 3: Login with Invalid Credentials
    print("3️⃣ Testing Login (Invalid Credentials)")
    try:
        response = requests.post(
            f"{url}/api/login",
            json={"username_or_email": "nonexistent", "password": "wrong"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ PASSED - Correctly rejected invalid credentials")
            tests_passed += 1
        elif response.status_code == 500:
            print("   ❌ FAILED - 500 error (database issue)")
            tests_failed += 1
        else:
            print(f"   ⚠️ UNEXPECTED - Got {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        tests_failed += 1
    print()
    
    # Test 4: Login with Valid Test User
    print("4️⃣ Testing Login (Valid Test User)")
    try:
        response = requests.post(
            f"{url}/api/login",
            json={"username_or_email": "testuser", "password": "Test123!"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ PASSED - Login successful")
            tests_passed += 1
        elif response.status_code == 401:
            print("   ⚠️ FAILED - Test user not found (expected before fix)")
            tests_failed += 1
        elif response.status_code == 500:
            print("   ❌ FAILED - 500 error (database issue)")
            tests_failed += 1
        else:
            print(f"   ⚠️ UNEXPECTED - Got {response.status_code}")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        tests_failed += 1
    print()
    
    # Summary
    print("=" * 50)
    print("📊 TEST SUMMARY")
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    
    if tests_failed > 0:
        print("\n🔧 RECOMMENDATIONS:")
        if "users table missing" in str(tests_failed):
            print("- Deploy database migrations using render-build.sh")
        if "500 error" in str(tests_failed):
            print("- Check database connection and schema")
        print("- Run this test again after deployment")
        return False
    else:
        print("\n🎉 All tests passed! Backend is working correctly.")
        return True

if __name__ == "__main__":
    # Default to the current backend URL
    backend_url = "https://prok-professional-networking-se45.onrender.com"
    
    if len(sys.argv) > 1:
        backend_url = sys.argv[1]
    
    success = test_backend(backend_url)
    sys.exit(0 if success else 1) 