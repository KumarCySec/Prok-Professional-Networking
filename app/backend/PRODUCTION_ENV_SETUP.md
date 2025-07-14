# 🚀 Production Environment Variables Setup

## Backend Environment Variables (Render Web Service)

Set these in your Render dashboard under Environment Variables:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-here-change-this
JWT_SECRET_KEY=your-jwt-secret-key-here-change-this

# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# CORS Configuration
ALLOWED_ORIGINS=https://prok-professional-networking-1-iv6a.onrender.com,http://localhost:5173

# Production Settings
FLASK_ENV=production
FLASK_DEBUG=false
```

## Frontend Environment Variables (Render Static Site)

Set these in your Render dashboard under Environment Variables:

```bash
# API Configuration
VITE_API_URL=https://prok-professional-networking-se45.onrender.com

# Build Configuration
NODE_ENV=production
```

## 🔧 Critical Configuration Notes

### 1. **CORS Origins**
- Must include your exact frontend URL
- Include localhost for development
- No trailing slashes

### 2. **Database URL**
- Render automatically provides `DATABASE_URL`
- Must be PostgreSQL for production
- Format: `postgresql://username:password@host:port/database_name`

### 3. **Secret Keys**
- Generate strong random keys
- Never commit to version control
- Use different keys for SECRET_KEY and JWT_SECRET_KEY

### 4. **Environment-Specific Settings**
- Set `FLASK_ENV=production` for backend
- Set `NODE_ENV=production` for frontend
- Disable debug mode in production

## 🛠️ Key Generation Commands

Generate secure secret keys:

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

## ✅ Validation Checklist

After setting environment variables:

- [ ] Backend starts without errors
- [ ] Frontend builds successfully
- [ ] CORS requests work from frontend to backend
- [ ] Database connections are established
- [ ] JWT tokens are generated and validated
- [ ] File uploads work correctly
- [ ] All API endpoints respond properly

## 🚨 Common Issues

1. **CORS Errors**: Check that frontend URL is in ALLOWED_ORIGINS
2. **Database Connection**: Verify DATABASE_URL format and credentials
3. **JWT Errors**: Ensure JWT_SECRET_KEY is set and consistent
4. **Build Failures**: Check that VITE_API_URL is correct
5. **Session Issues**: Verify SECRET_KEY is set and unique 