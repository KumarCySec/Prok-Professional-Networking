#!/usr/bin/env python3

from app import app
from models.user import User

app.app_context().push()

user = User.find_by_username('Kishore')
if user:
    print(f"User found: {user.username}")
    
    # Test common passwords
    test_passwords = [
        "Test123!",
        "TestPass123!",
        "DebugPass123!",
        "password",
        "123456",
        "admin",
        "test"
    ]
    
    for password in test_passwords:
        result = user.check_password(password)
        print(f"Password '{password}': {result}")
        if result:
            print(f"✅ Found correct password: {password}")
            break
else:
    print("User 'Kishore' not found") 