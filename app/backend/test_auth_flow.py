#!/usr/bin/env python3
"""
Test script to verify authentication flow and profile image updates
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_auth_flow():
    """Test the complete authentication flow"""
    print("🔍 Testing Authentication Flow...")
    
    # Test 1: Login
    print("\n1. Testing Login...")
    login_data = {
        "username_or_email": "testuser",
        "password": "TestPass123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            print(f"✅ Login successful!")
            print(f"   Token: {token[:20]}...")
            print(f"   User: {user.get('username')}")
            print(f"   Profile Image: {user.get('profile_image_url', 'None')}")
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None
    
    # Test 2: Get current user
    print("\n2. Testing /api/me endpoint...")
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(f"{BASE_URL}/api/me", headers=headers)
        print(f"GET /api/me Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            user = data.get('user')
            print(f"✅ /api/me successful!")
            print(f"   User: {user.get('username')}")
            print(f"   Profile Image: {user.get('profile_image_url', 'None')}")
            print(f"   First Name: {user.get('first_name', 'None')}")
            print(f"   Last Name: {user.get('last_name', 'None')}")
        else:
            print(f"❌ /api/me failed: {response.text}")
            
    except Exception as e:
        print(f"❌ /api/me error: {e}")
    
    # Test 3: Get profile
    print("\n3. Testing /api/profile endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
        print(f"GET /api/profile Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            profile = data.get('profile')
            print(f"✅ /api/profile successful!")
            print(f"   Profile Image: {profile.get('profile_image_url', 'None')}")
            print(f"   First Name: {profile.get('first_name', 'None')}")
            print(f"   Last Name: {profile.get('last_name', 'None')}")
        else:
            print(f"❌ /api/profile failed: {response.text}")
            
    except Exception as e:
        print(f"❌ /api/profile error: {e}")
    
    return token

def test_profile_update():
    """Test profile update functionality"""
    print("\n🔍 Testing Profile Update...")
    
    # First login to get token
    token = test_auth_flow()
    if not token:
        print("❌ Cannot test profile update without valid token")
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test profile update
    print("\n4. Testing Profile Update...")
    update_data = {
        "first_name": "Test",
        "last_name": "User",
        "bio": "This is a test bio"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/profile", 
                              json=update_data, 
                              headers=headers)
        print(f"PUT /api/profile Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            profile = data.get('profile')
            print(f"✅ Profile update successful!")
            print(f"   First Name: {profile.get('first_name')}")
            print(f"   Last Name: {profile.get('last_name')}")
            print(f"   Bio: {profile.get('bio')}")
        else:
            print(f"❌ Profile update failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Profile update error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Authentication Flow Test...")
    print("=" * 50)
    
    test_auth_flow()
    test_profile_update()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!") 