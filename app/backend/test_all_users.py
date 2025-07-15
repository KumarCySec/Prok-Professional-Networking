#!/usr/bin/env python3

from app import app
from models.user import User

app.app_context().push()

users = User.query.all()
print(f"Testing {len(users)} users with password 'Test123!':")
print("-" * 50)

for user in users:
    result = user.check_password("Test123!")
    print(f"{user.username}: {result}")
    if result:
        print(f"✅ Found working user: {user.username}")
        break

print("-" * 50)
print("Testing with 'TestPass123!':")
print("-" * 50)

for user in users:
    result = user.check_password("TestPass123!")
    print(f"{user.username}: {result}")
    if result:
        print(f"✅ Found working user: {user.username}")
        break 