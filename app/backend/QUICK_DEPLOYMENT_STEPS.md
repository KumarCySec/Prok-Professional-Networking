# Quick Deployment Steps for Render Database

## 🚀 Fast Track Deployment

### Step 1: Run the Deployment Script
```bash
./deploy_to_render.sh
```

### Step 2: Create PostgreSQL Database on Render
1. Go to https://render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `prok-database`
   - **Database**: `prok_db`
   - **Plan**: Free (for development)
4. Click "Create Database"

### Step 3: Get Database URL
- Copy the **External Database URL** from Render
- Format: `postgresql://user:password@host:port/prok_db`

### Step 4: Update Environment Variables
In your Render web service, add:
```bash
DATABASE_URL=postgresql://user:password@host:port/prok_db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
FLASK_DEBUG=False
```

### Step 5: Deploy Application
1. Create new "Web Service" on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variables from Step 4
6. Deploy!

### Step 6: Test Deployment
```bash
# Test health endpoint
curl https://your-app.onrender.com/api/health

# Test database connection
curl https://your-app.onrender.com/api/db-test
```

## 📋 What's Already Configured

✅ **PostgreSQL Support**: Your `config.py` already handles PostgreSQL URLs
✅ **Dependencies**: `psycopg2-binary` is in `requirements.txt`
✅ **Migrations**: Flask-Migrate is configured
✅ **Procfile**: Ready for Render deployment
✅ **CORS**: Configured for cross-origin requests

## 🔧 Local Testing

To test with Render database locally:
```bash
export DATABASE_URL="postgresql://user:password@host:port/prok_db"
flask run
```

## 📖 Full Documentation

For detailed instructions, see: `RENDER_DATABASE_DEPLOYMENT.md`

## 🆘 Troubleshooting

**Connection Issues**: Add `?sslmode=require` to DATABASE_URL
**Migration Errors**: Run `flask db upgrade` manually
**Build Failures**: Check `requirements.txt` and Python version

---
**Need Help?** Check the full deployment guide or Render documentation. 