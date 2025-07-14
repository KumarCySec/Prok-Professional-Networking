# 🔧 Backend 500 Error Fix Guide

## 🎯 Problem
The login endpoint `/api/login` is returning a 500 Internal Server Error on the production server.

## 🔍 Root Cause Analysis
The 500 error is likely caused by:
1. **Database tables not created** on the production server
2. **Database connection issues**
3. **Missing environment variables**
4. **Migration not run** on production

## ✅ Solution Steps

### 1. **Check Database Connection**
Run the database connection test:
```bash
cd app/backend
python test_db_connection.py
```

### 2. **Initialize Database (if needed)**
If the test fails, run the database initialization:
```bash
cd app/backend
python init_database.py
```

### 3. **Debug Login Endpoint**
Run the debug script to identify specific issues:
```bash
cd app/backend
python debug_login.py
```

### 4. **Check Environment Variables**
Ensure these environment variables are set on Render:
```bash
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
```

### 5. **Run Migrations**
If using Flask-Migrate, run migrations:
```bash
cd app/backend
flask db upgrade
```

## 🚀 Production Deployment Fix

### Option 1: Manual Database Setup
1. **SSH into your Render server** (if possible)
2. **Run the initialization script**:
   ```bash
   python init_database.py
   ```
3. **Restart the application**

### Option 2: Render Build Command
Add database initialization to your build command in Render:
```bash
python init_database.py && gunicorn app:app --bind 0.0.0.0:$PORT
```

### Option 3: Environment Variable Fix
Check your Render dashboard for:
- `DATABASE_URL` - Should point to your production database
- `SECRET_KEY` - Should be a secure random string
- `JWT_SECRET_KEY` - Should be a secure random string
- `ALLOWED_ORIGINS` - Should include your frontend URL

## 🔧 Quick Fix Script

Create a `setup.py` file in your backend directory:

```python
#!/usr/bin/env python3
"""
Quick setup script for production
"""

import os
import sys
from flask import Flask

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from extensions import db
from models.user import User

def quick_setup():
    """Quick database setup"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("✅ Tables created")
        
        # Test connection
        from sqlalchemy import text
        result = db.session.execute(text('SELECT 1'))
        print("✅ Database connection working")
        
        return True

if __name__ == "__main__":
    quick_setup()
```

## 🧪 Testing After Fix

1. **Test the health endpoint**:
   ```bash
   curl https://prok-professional-networking-se45.onrender.com/
   ```

2. **Test the login endpoint**:
   ```bash
   curl -X POST https://prok-professional-networking-se45.onrender.com/api/login \
     -H "Content-Type: application/json" \
     -d '{"username_or_email":"test","password":"test123"}'
   ```

3. **Check the frontend** - Try logging in with a valid user

## 🛠️ Troubleshooting

### If still getting 500 errors:

1. **Check Render logs** in the dashboard
2. **Verify database URL** is correct
3. **Ensure all environment variables** are set
4. **Check if database service** is running
5. **Verify CORS settings** are correct

### Common Issues:

- **Database URL format**: Should be `postgresql://` not `postgres://`
- **Missing tables**: Run `db.create_all()` or migrations
- **CORS issues**: Check `ALLOWED_ORIGINS` environment variable
- **Memory issues**: Check if the database connection is being closed properly

## 📝 Notes

- The 500 error suggests a server-side issue, not a frontend problem
- Database initialization is the most likely cause
- Environment variables must be set correctly in Render dashboard
- The frontend is correctly configured to call the backend API 