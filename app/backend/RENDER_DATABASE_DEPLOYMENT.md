# Render Database Deployment Guide

This guide will walk you through deploying your PostgreSQL database to Render and connecting your Flask application to it.

## Prerequisites

- A Render account (free tier available)
- Your Flask application code ready for deployment
- Git repository connected to Render

## Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard**
   - Visit https://render.com
   - Sign in to your account

2. **Create New PostgreSQL Service**
   - Click "New +" button
   - Select "PostgreSQL"
   - Choose "Create New Database"

3. **Configure Database**
   - **Name**: `prok-database` (or your preferred name)
   - **Database**: `prok_db`
   - **User**: `prok_user` (or auto-generated)
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 15 (latest stable)
   - **Plan**: Free (for development) or Starter ($7/month for production)

4. **Create Database**
   - Click "Create Database"
   - Wait for provisioning (usually 1-2 minutes)

## Step 2: Get Database Connection Details

After creation, Render will provide:

- **Internal Database URL**: `postgresql://user:password@host:port/database`
- **External Database URL**: `postgresql://user:password@host:port/database`
- **Database Name**: `prok_db`
- **User**: `prok_user`
- **Password**: (auto-generated)
- **Host**: `host.render.com`
- **Port**: `5432`

**Important**: Save these details securely!

## Step 3: Update Environment Variables

In your Render web service, add these environment variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/prok_db

# Flask Configuration
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_DEBUG=False

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:5173

# Logging
LOG_LEVEL=INFO
```

## Step 4: Update Your Application

Your `config.py` already supports PostgreSQL. The key part is:

```python
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = DATABASE_URL or f'mysql://root:{default_password}@localhost/prok_db'
```

## Step 5: Database Migration and Setup

### Option A: Using Flask-Migrate (Recommended)

1. **Initialize Migrations** (if not already done):
   ```bash
   flask db init
   ```

2. **Create Migration**:
   ```bash
   flask db migrate -m "Initial database setup"
   ```

3. **Apply Migration**:
   ```bash
   flask db upgrade
   ```

### Option B: Using the Setup Script

Run the provided setup script:

```bash
python create_render_database.py
```

## Step 6: Deploy Your Application

1. **Connect Repository**
   - In Render, create a new "Web Service"
   - Connect your GitHub/GitLab repository
   - Select the repository containing your Flask app

2. **Configure Build Settings**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

3. **Set Environment Variables**
   - Add all the environment variables from Step 3
   - Make sure `DATABASE_URL` points to your Render PostgreSQL database

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

## Step 7: Verify Deployment

1. **Check Application Health**
   - Visit your application URL
   - Test the `/api/health` endpoint
   - Test the `/api/db-test` endpoint

2. **Test Database Connection**
   ```bash
   curl https://your-app.onrender.com/api/db-test
   ```

3. **Test Authentication**
   - Try creating a new user account
   - Test login functionality

## Step 8: Database Management

### Accessing Your Database

1. **Via Render Dashboard**
   - Go to your PostgreSQL service
   - Click "Connect" → "External Database URL"
   - Use a PostgreSQL client (pgAdmin, DBeaver, etc.)

2. **Via Command Line**
   ```bash
   psql "postgresql://user:password@host:port/prok_db"
   ```

### Backup and Restore

1. **Create Backup**:
   ```bash
   pg_dump "postgresql://user:password@host:port/prok_db" > backup.sql
   ```

2. **Restore Backup**:
   ```bash
   psql "postgresql://user:password@host:port/prok_db" < backup.sql
   ```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if database is running
   - Verify connection string
   - Ensure firewall allows connections

2. **Authentication Failed**
   - Verify username/password
   - Check if user has proper permissions

3. **Migration Errors**
   - Check if tables already exist
   - Verify migration files are correct
   - Check database permissions

4. **SSL Connection Issues**
   - Add `?sslmode=require` to DATABASE_URL
   - Example: `postgresql://user:pass@host:port/db?sslmode=require`

### Debug Commands

```bash
# Test database connection
python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.environ['DATABASE_URL'])
print('Connection successful!')
"

# Check tables
python -c "
from app import create_app
from extensions import db
app = create_app()
with app.app_context():
    result = db.session.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \\'public\\'')
    for row in result:
        print(row[0])
"
```

## Security Best Practices

1. **Environment Variables**
   - Never commit secrets to Git
   - Use Render's environment variable system
   - Rotate secrets regularly

2. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Restrict access to necessary IPs only

3. **Application Security**
   - Use HTTPS in production
   - Implement proper CORS policies
   - Validate all user inputs

## Cost Optimization

1. **Free Tier Limits**
   - 1GB storage
   - 90 days of inactivity before suspension
   - Limited bandwidth

2. **Upgrading to Paid**
   - Starter plan: $7/month
   - Includes 1GB storage, daily backups
   - Better performance and reliability

## Monitoring

1. **Render Dashboard**
   - Monitor database usage
   - Check connection logs
   - View performance metrics

2. **Application Logs**
   - Check your Flask app logs
   - Monitor database queries
   - Watch for errors

## Next Steps

1. **Set up automated backups**
2. **Implement database monitoring**
3. **Optimize queries and indexes**
4. **Set up staging environment**
5. **Implement CI/CD pipeline**

---

**Need Help?**
- Render Documentation: https://render.com/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/ 