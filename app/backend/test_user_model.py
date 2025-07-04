#!/usr/bin/env python3
"""
Test script for User model functionality
This script demonstrates the User model features and validates all requirements.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Create a minimal Flask app for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import the User model
from models.user import User

def test_password_complexity():
    """Test password complexity validation"""
    print("Testing password complexity validation...")
    
    # Test valid password
    valid_password = "SecurePass123!"
    user = User(username="testuser", email="test@example.com", password=valid_password)
    print(f"✅ Valid password '{valid_password}' accepted")
    
    # Test invalid passwords
    invalid_passwords = [
        "short",  # Too short
        "nouppercase123!",  # No uppercase
        "NOLOWERCASE123!",  # No lowercase
        "NoDigits!",  # No digits
        "NoSpecial123"  # No special characters
    ]
    
    for password in invalid_passwords:
        try:
            User(username="testuser", email="test@example.com", password=password)
            print(f"❌ Invalid password '{password}' was accepted (should have failed)")
        except ValueError as e:
            print(f"✅ Invalid password '{password}' correctly rejected: {e}")

def test_username_validation():
    """Test username validation"""
    print("\nTesting username validation...")
    
    # Test valid usernames
    valid_usernames = ["user123", "test_user", "MyUser", "user_123"]
    for username in valid_usernames:
        if User._validate_username_static(username):
            print(f"✅ Valid username '{username}' accepted")
        else:
            print(f"❌ Valid username '{username}' rejected")
    
    # Test invalid usernames
    invalid_usernames = ["ab", "verylongusername123456789", "user@name", "user-name", "user name"]
    for username in invalid_usernames:
        if not User._validate_username_static(username):
            print(f"✅ Invalid username '{username}' correctly rejected")
        else:
            print(f"❌ Invalid username '{username}' was accepted (should have failed)")

def test_email_validation():
    """Test email validation"""
    print("\nTesting email validation...")
    
    # Test valid emails
    valid_emails = ["test@example.com", "user.name@domain.co.uk", "user+tag@example.org"]
    for email in valid_emails:
        if User._validate_email_static(email):
            print(f"✅ Valid email '{email}' accepted")
        else:
            print(f"❌ Valid email '{email}' rejected")
    
    # Test invalid emails
    invalid_emails = ["invalid-email", "@example.com", "user@", "user.example.com"]
    for email in invalid_emails:
        if not User._validate_email_static(email):
            print(f"✅ Invalid email '{email}' correctly rejected")
        else:
            print(f"❌ Invalid email '{email}' was accepted (should have failed)")

def test_password_hashing():
    """Test password hashing functionality"""
    print("\nTesting password hashing...")
    
    password = "SecurePass123!"
    user = User(username="testuser", email="test@example.com", password=password)
    
    # Test password verification
    if user.check_password(password):
        print("✅ Password verification works correctly")
    else:
        print("❌ Password verification failed")
    
    # Test wrong password
    if not user.check_password("WrongPassword123!"):
        print("✅ Wrong password correctly rejected")
    else:
        print("❌ Wrong password was accepted")

def test_user_creation():
    """Test user creation with validation"""
    print("\nTesting user creation...")
    
    with app.app_context():
        db.create_all()
        
        try:
            # Create a valid user
            user = User.create_user(
                username="newuser",
                email="newuser@example.com",
                password="SecurePass123!"
            )
            db.session.add(user)
            db.session.commit()
            print("✅ User created successfully")
            
            # Test duplicate username
            try:
                User.create_user(
                    username="newuser",  # Same username
                    email="different@example.com",
                    password="SecurePass123!"
                )
                print("❌ Duplicate username was accepted (should have failed)")
            except ValueError as e:
                print(f"✅ Duplicate username correctly rejected: {e}")
            
            # Test duplicate email
            try:
                User.create_user(
                    username="differentuser",
                    email="newuser@example.com",  # Same email
                    password="SecurePass123!"
                )
                print("❌ Duplicate email was accepted (should have failed)")
            except ValueError as e:
                print(f"✅ Duplicate email correctly rejected: {e}")
                
        except Exception as e:
            print(f"❌ User creation failed: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing User Model Implementation")
    print("=" * 50)
    
    test_password_complexity()
    test_username_validation()
    test_email_validation()
    test_password_hashing()
    test_user_creation()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 