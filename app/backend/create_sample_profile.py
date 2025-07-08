#!/usr/bin/env python3
"""
Script to create a sample profile for testing the profile system.
This will create a user account and profile with realistic data that can be used to test the edit functionality.
"""

import requests
import json
import time

# Backend API base URL
BASE_URL = "http://localhost:5000"

def create_user_account():
    """Create a test user account"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    
    try:
        print("Creating user account...")
        response = requests.post(
            f"{BASE_URL}/api/signup",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ User account created successfully!")
            return result.get('access_token')
        else:
            print(f"⚠️ User creation response: {response.status_code}")
            if response.status_code == 400:
                # User might already exist, try to login
                print("User might already exist, trying to login...")
                return login_user(user_data)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating user: {e}")
        return None

def login_user(user_data):
    """Login with existing user credentials"""
    login_data = {
        "username_or_email": user_data["username"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            return result.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error logging in: {e}")
        return None

def create_sample_profile(token):
    """Create a sample profile with realistic data"""
    
    # Sample profile data
    profile_data = {
        "first_name": "John",
        "last_name": "Doe",
        "bio": "Passionate software engineer with 5+ years of experience in full-stack development. I love building scalable applications and solving complex problems. Currently working on exciting projects in the fintech space.",
        "location": "San Francisco, CA",
        "company": "TechCorp Inc.",
        "job_title": "Senior Software Engineer",
        "website": "https://johndoe.dev",
        "phone": "+1 (555) 123-4567",
        "headline": "Senior Software Engineer | Full-Stack Developer | Tech Enthusiast",
        "industry": "Technology",
        "current_position": "Senior Software Engineer",
        "company_size": "201-500",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "twitter_url": "https://twitter.com/johndoe",
        "github_url": "https://github.com/johndoe",
        "experience_years": 5,
        "skills": ["JavaScript", "React", "Node.js", "Python", "PostgreSQL", "AWS", "Docker", "Kubernetes"],
        "education": [
            {
                "degree": "Bachelor of Science in Computer Science",
                "institution": "Stanford University",
                "year": "2019"
            },
            {
                "degree": "Master of Science in Software Engineering",
                "institution": "UC Berkeley",
                "year": "2021"
            }
        ],
        "social_links": {
            "portfolio": "https://johndoe.dev",
            "blog": "https://blog.johndoe.dev"
        },
        "is_public": True,
        "allow_messages": True,
        "show_email": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # First, let's check if profile already exists
        print("Checking if profile exists...")
        response = requests.get(f"{BASE_URL}/api/profile", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ User profile already exists!")
            existing_profile = response.json()
            print(f"Current profile: {existing_profile.get('first_name', 'Unknown')} {existing_profile.get('last_name', 'Unknown')}")
            return existing_profile
        elif response.status_code == 404:
            print("❌ No profile found. Creating new profile...")
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking profile: {e}")
        return None
    
    try:
        # Create the profile
        print("Creating profile...")
        response = requests.post(
            f"{BASE_URL}/api/profile",
            json=profile_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            created_profile = response.json()
            print("✅ Profile created successfully!")
            print(f"Profile ID: {created_profile.get('id')}")
            print(f"Name: {created_profile.get('first_name')} {created_profile.get('last_name')}")
            print(f"Headline: {created_profile.get('headline')}")
            return created_profile
        else:
            print(f"❌ Failed to create profile: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating profile: {e}")
        return None

def update_profile_with_image():
    """Update the profile with a sample image (if available)"""
    try:
        # This would require an actual image file
        # For now, we'll just update some fields
        update_data = {
            "bio": "Updated bio: Experienced software engineer passionate about building innovative solutions. I specialize in React, Node.js, and cloud technologies. Always eager to learn new technologies and contribute to meaningful projects.",
            "skills": ["JavaScript", "React", "Node.js", "Python", "PostgreSQL", "AWS", "Docker", "Kubernetes", "TypeScript", "GraphQL"]
        }
        
        response = requests.put(
            f"{BASE_URL}/api/profile",
            json=update_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Profile updated successfully!")
            return response.json()
        else:
            print(f"❌ Failed to update profile: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating profile: {e}")
        return None

def main():
    """Main function to create and setup the sample profile"""
    print("🚀 Setting up sample profile for testing...")
    print("=" * 50)
    
    # Wait a moment for backend to be ready
    print("Waiting for backend to be ready...")
    time.sleep(2)
    
    # First create/get user account and get token
    token = create_user_account()
    
    if not token:
        print("❌ Failed to get authentication token")
        return
    
    print(f"✅ Got authentication token: {token[:20]}...")
    
    # Create the profile
    profile = create_sample_profile(token)
    
    if profile:
        print("\n" + "=" * 50)
        print("✅ Sample profile setup complete!")
        print("\nYou can now:")
        print("1. Visit http://localhost:5174/login")
        print("2. Login with username: 'testuser' and password: 'TestPass123!'")
        print("3. Visit http://localhost:5174/profile to view the profile")
        print("4. Click 'Edit Profile' to test the edit functionality")
        print("5. Modify any fields and save changes")
        print("\nProfile details:")
        print(f"  Name: {profile.get('first_name', 'N/A')} {profile.get('last_name', 'N/A')}")
        print(f"  Headline: {profile.get('headline', 'N/A')}")
        print(f"  Company: {profile.get('company', 'N/A')}")
        print(f"  Location: {profile.get('location', 'N/A')}")
        print(f"  Skills: {', '.join(profile.get('skills', []))}")
    else:
        print("\n❌ Failed to setup sample profile")
        print("Please check that:")
        print("1. Backend server is running on http://localhost:5000")
        print("2. Database is properly configured")
        print("3. All required tables exist")

if __name__ == "__main__":
    main() 