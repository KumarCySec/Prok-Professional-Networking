# 🚀 Deployment Checklist

## Current Status: ❌ DATABASE NOT CONFIGURED

The error `sqlite3.OperationalError` means your app is still using SQLite instead of PostgreSQL.

## ✅ Step-by-Step Fix

### 1. Create PostgreSQL Database
- [ ] Go to [Render Dashboard](https://dashboard.render.com)
- [ ] Click **"New"** → **"PostgreSQL"**
- [ ] Name: `prok-database`
- [ ] Plan: Free
- [ ] Click **"Create Database"**

### 2. Get Database URL
- [ ] Click on your new PostgreSQL database
- [ ] Copy the **"External Database URL"**
- [ ] Should look like: `postgresql://user:password@host:port/database`

### 3. Update Backend Environment Variables
- [ ] Go to your backend service: `prok-professional-networking-dvec`
- [ ] Click **"Environment"** tab
- [ ] Add/Update these variables:

```
DATABASE_URL = [Paste the PostgreSQL URL from Step 2]
SECRET_KEY = my-super-secret-key-change-this-in-production-12345
JWT_SECRET_KEY = jwt-super-secret-key-change-this-in-production-67890
ALLOWED_ORIGINS = https://prok-professional-networking-dvec.onrender.com,https://prok-frontend-4h1s.onrender.com,http://localhost:5173
```

### 4. Redeploy
- [ ] Click **"Save Changes"**
- [ ] Go to **"Manual Deploy"** tab
- [ ] Click **"Deploy latest commit"**
- [ ] Wait for deployment to complete

### 5. Test
- [ ] Test database: `curl https://prok-professional-networking-dvec.onrender.com/api/db-test`
- [ ] Should return success, not SQLite error
- [ ] Test signup/login in your frontend

## 🧪 Test Commands

```bash
# Test database connection
curl https://prok-professional-networking-dvec.onrender.com/api/db-test

# Test signup
curl -X POST https://prok-professional-networking-dvec.onrender.com/api/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test123!"}'

# Test login
curl -X POST https://prok-professional-networking-dvec.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username_or_email":"testuser","password":"Test123!"}'
```

## 🚨 Common Issues

### Issue: Still getting SQLite error
**Solution**: `DATABASE_URL` is not set correctly. Double-check the environment variable.

### Issue: Database connection failed
**Solution**: PostgreSQL database might not be running. Check the database service status.

### Issue: CORS errors
**Solution**: Frontend URL not in `ALLOWED_ORIGINS`. Verify the URL is correct.

## 📞 Need Help?

1. Check Render deployment logs
2. Verify environment variables are set
3. Ensure PostgreSQL database is running
4. Test endpoints with curl commands above

## ✅ Success Indicators

- `/api/db-test` returns success with user count
- No more `sqlite3.OperationalError`
- Login/signup works without 503 errors
- Frontend can connect to backend successfully 