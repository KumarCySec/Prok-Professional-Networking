# Backend Deployment Configuration

## Environment Variables

Set the following environment variables in your deployment platform:

```env
# Flask Secret Key (generate a strong random key)
SECRET_KEY=your-super-secret-key-here

# JWT Secret Key (generate a strong random key)
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database URL (for cloud databases like PostgreSQL)
DATABASE_URL=postgresql://username:password@host:port/database_name

# CORS Allowed Origins (comma-separated list)
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app,https://your-frontend-url.netlify.app

# Example for local development
# ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Database Configuration

### PostgreSQL (Recommended for production)
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### MySQL (Local development)
```env
DATABASE_URL=mysql://root:password@localhost/prok_db
```

## Deployment Platforms

### Render
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`

### Railway
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Add `gunicorn` to requirements.txt
4. Start command: `gunicorn app:app`

### Heroku
1. Connect your GitHub repository
2. Set environment variables in Heroku dashboard
3. Add `gunicorn` to requirements.txt
4. Create `Procfile` with: `web: gunicorn app:app`

## Required Files

### requirements.txt
Make sure your requirements.txt includes:
```
gunicorn
flask-cors
flask-jwt-extended
flask-sqlalchemy
flask-migrate
# ... other dependencies
```

### Procfile (for Heroku)
```
web: gunicorn app:app
```

## Database Migration

After deployment, run database migrations:
```bash
flask db upgrade
``` 