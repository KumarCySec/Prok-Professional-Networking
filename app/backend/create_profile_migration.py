#!/usr/bin/env python3
"""
Script to create a migration for profile fields added to User model
Run this locally to generate the migration, then commit and deploy
"""

import os
import sys
import subprocess

def create_profile_migration():
    """Create a new migration for profile fields"""
    try:
        print("🚀 Creating migration for profile fields...")
        
        # Set Flask environment
        os.environ['FLASK_APP'] = 'app.py'
        
        # Create the migration
        result = subprocess.run([
            'flask', 'db', 'migrate', '-m', 'Add profile fields to User model'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print("✅ Migration created successfully")
            print("📝 Migration output:")
            print(result.stdout)
            
            # List migration files
            migrations_dir = os.path.join(os.path.dirname(__file__), 'migrations', 'versions')
            if os.path.exists(migrations_dir):
                migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py')]
                print(f"📁 Migration files: {migration_files}")
            
            print("\n📋 Next steps:")
            print("1. Review the generated migration file")
            print("2. Commit the migration to your repository")
            print("3. Deploy to Render")
            print("4. The migration will run automatically during deployment")
            
            return True
        else:
            print("❌ Failed to create migration")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error creating migration: {e}")
        return False

def test_migration():
    """Test the migration locally"""
    try:
        print("\n🧪 Testing migration locally...")
        
        # Set Flask environment
        os.environ['FLASK_APP'] = 'app.py'
        
        # Run the migration
        result = subprocess.run([
            'flask', 'db', 'upgrade'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print("✅ Migration test successful")
            print("📝 Migration output:")
            print(result.stdout)
            return True
        else:
            print("❌ Migration test failed")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error testing migration: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Profile Migration Tool")
    print("=" * 40)
    
    # Create migration
    if create_profile_migration():
        # Test migration
        test_migration()
    else:
        print("❌ Failed to create migration")
        sys.exit(1) 