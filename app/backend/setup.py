#!/usr/bin/env python3
"""
Setup script for Flask application
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask-sqlalchemy', 
        'flask-migrate',
        'flask-cors',
        'werkzeug',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = '.env'
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    env_content = """# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=1

# Database Configuration
DATABASE_URL=mysql://root:Kumar@249@localhost/prok_db

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# CORS Configuration
CORS_HEADERS=Content-Type
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️  Please update the database credentials in .env file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def setup_database():
    """Setup database migrations"""
    print("🗄️  Setting up database...")
    
    # Set Flask app environment variable
    os.environ['FLASK_APP'] = 'app.py'
    
    # Initialize migrations
    if not run_command("flask db init", "Initializing database migrations"):
        return False
    
    # Create initial migration
    if not run_command('flask db migrate -m "Add User model"', "Creating initial migration"):
        return False
    
    # Apply migration
    if not run_command("flask db upgrade", "Applying database migration"):
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Flask Application Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Please run this script from the backend directory")
        sys.exit(1)
    
    success = True
    success &= check_dependencies()
    success &= create_env_file()
    success &= setup_database()
    
    print("=" * 50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Update database credentials in .env file")
        print("2. Run the application: flask run")
        print("3. Test the setup: python test_setup.py")
    else:
        print("❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 