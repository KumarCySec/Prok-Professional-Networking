#!/usr/bin/env python3
"""
Test script to verify Flask application setup
"""

def test_imports():
    """Test that all imports work correctly"""
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Flask-SQLAlchemy imported successfully")
        
        from flask_migrate import Migrate
        print("✅ Flask-Migrate imported successfully")
        
        from werkzeug.security import generate_password_hash, check_password_hash
        print("✅ Werkzeug security imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created"""
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def test_user_model():
    """Test that the User model can be imported and used"""
    try:
        from models.user import User
        print("✅ User model imported successfully")
        
        # Test password validation
        test_password = "TestPass123!"
        user = User("testuser", "test@example.com", test_password)
        print("✅ User model instantiated successfully")
        
        # Test password checking
        assert user.check_password(test_password)
        print("✅ Password hashing and checking works")
        
        return True
    except Exception as e:
        print(f"❌ User model error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Flask application setup...")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_app_creation()
    success &= test_user_model()
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Application is ready to run.")
        print("\nTo run the application:")
        print("export FLASK_APP=app.py")
        print("flask run")
        print("\nTo initialize database migrations:")
        print("flask db init")
        print("flask db migrate -m 'Add User model'")
        print("flask db upgrade")
    else:
        print("❌ Some tests failed. Please check the errors above.") 