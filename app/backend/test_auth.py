#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_signup():
    """Test user registration"""
    print("🧪 Testing Signup Endpoint...")
    
    # Test valid signup
    data = {
        "username": "testuser_api",
        "email": "testapi@example.com",
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/api/signup", json=data)
    print(f"✅ Valid signup: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"   User ID: {result['user']['id']}")
        print(f"   Token: {result['access_token'][:20]}...")
        return result['access_token']
    
    return None

def test_login():
    """Test user login"""
    print("\n🧪 Testing Login Endpoint...")
    
    # Test valid login
    data = {
        "username_or_email": "testuser_api",
        "password": "TestPass123!"
    }
    
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    print(f"✅ Valid login: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   User ID: {result['user']['id']}")
        print(f"   Token: {result['access_token'][:20]}...")
        return result['access_token']
    
    return None

def test_protected_endpoint(token):
    """Test protected endpoint"""
    print("\n🧪 Testing Protected Endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/me", headers=headers)
    print(f"✅ Protected endpoint: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   User: {result['user']['username']}")

def test_validation_errors():
    """Test validation errors"""
    print("\n🧪 Testing Validation Errors...")
    
    # Test weak password
    data = {
        "username": "testuser_weak",
        "email": "weak@example.com",
        "password": "weak"
    }
    response = requests.post(f"{BASE_URL}/api/signup", json=data)
    print(f"❌ Weak password: {response.status_code} - {response.json().get('error', '')}")
    
    # Test duplicate username
    data = {
        "username": "testuser_api",
        "email": "duplicate@example.com",
        "password": "TestPass123!"
    }
    response = requests.post(f"{BASE_URL}/api/signup", json=data)
    print(f"❌ Duplicate username: {response.status_code} - {response.json().get('error', '')}")
    
    # Test invalid login
    data = {
        "username_or_email": "testuser_api",
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    print(f"❌ Invalid login: {response.status_code} - {response.json().get('error', '')}")

if __name__ == "__main__":
    print("🚀 Authentication API Test Suite")
    print("=" * 50)
    
    try:
        # Test signup
        token = test_signup()
        
        # Test login
        login_token = test_login()
        
        # Test protected endpoint
        if token:
            test_protected_endpoint(token)
        
        # Test validation errors
        test_validation_errors()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Flask is running on localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {e}")
