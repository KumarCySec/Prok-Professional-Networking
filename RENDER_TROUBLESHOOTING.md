# Render Deployment Troubleshooting Guide

## Issue: "Not Found" Error on Both Frontend and Backend

### Step 1: Check Render Service Status

1. **Go to your Render Dashboard**
2. **Check both services:**
   - Are they showing as "Live" (green status)?
   - Are there any error messages in the logs?

### Step 2: Backend Configuration Issues

#### Check Backend Service Configuration:
1. **Service Type:** Should be "Web Service"
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `gunicorn app:app`
4. **Root Directory:** `app/backend` (if your repo structure has the backend in a subdirectory)

#### Common Backend Issues:
- **Wrong start command:** Should be `gunicorn app:app` not `python app.py`
- **Missing dependencies:** Check if `gunicorn` is in `requirements.txt`
- **Port configuration:** Render automatically sets `PORT` environment variable

### Step 3: Frontend Configuration Issues

#### Check Frontend Service Configuration:
1. **Service Type:** Should be "Static Site"
2. **Build Command:** `npm install && npm run build`
3. **Publish Directory:** `dist`
4. **Root Directory:** `app/frontend` (if your repo structure has the frontend in a subdirectory)

#### Common Frontend Issues:
- **Wrong service type:** Should be "Static Site" not "Web Service"
- **Wrong publish directory:** Should be `dist` not `build`
- **Missing environment variables:** `VITE_API_URL` not set

### Step 4: Environment Variables

#### Backend Environment Variables (Required):
```env
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database_name
ALLOWED_ORIGINS=https://your-frontend-url.onrender.com
```

#### Frontend Environment Variables (Required):
```env
VITE_API_URL=https://your-backend-url.onrender.com
```

### Step 5: Database Configuration

1. **Check if your database is connected:**
   - Go to your backend service logs
   - Look for database connection errors
   - Make sure `DATABASE_URL` is set correctly

2. **Run migrations:**
   - Add this to your build command: `pip install -r requirements.txt && flask db upgrade`

### Step 6: Testing Your Services

#### Test Backend:
1. **Health Check:** Visit `https://your-backend-url.onrender.com/`
   - Should return: `{"status": "ok", "message": "Backend is running"}`

2. **API Health Check:** Visit `https://your-backend-url.onrender.com/api/health`
   - Should return: `{"status": "ok", "message": "API is running"}`

#### Test Frontend:
1. **Visit your frontend URL**
2. **Open browser developer tools**
3. **Check console for errors**
4. **Use the test-connection.html file to test API connectivity**

### Step 7: Common Solutions

#### If Backend Shows "Not Found":
1. **Check start command:** Should be `gunicorn app:app`
2. **Check file structure:** Make sure `app.py` exists in the root directory
3. **Check logs:** Look for import errors or missing dependencies

#### If Frontend Shows "Not Found":
1. **Check service type:** Should be "Static Site"
2. **Check publish directory:** Should be `dist`
3. **Check build logs:** Look for build errors

#### If Services Are Live But Not Working:
1. **Check environment variables**
2. **Check CORS configuration**
3. **Check database connection**
4. **Check API endpoints**

### Step 8: Debugging Commands

#### Check Backend Logs:
```bash
# In Render dashboard, check the logs for:
- Import errors
- Database connection errors
- Port binding errors
- Missing environment variables
```

#### Check Frontend Build:
```bash
# Locally test the build:
cd app/frontend
npm install
npm run build
# Check if dist/ folder is created successfully
```

### Step 9: Quick Fixes

#### For Backend:
1. **Update Procfile:**
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

2. **Add runtime.txt:**
   ```
   python-3.11.0
   ```

#### For Frontend:
1. **Add _redirects file (for SPA routing):**
   ```
   /*    /index.html   200
   ```

2. **Check vite.config.ts:**
   ```typescript
   export default defineConfig({
     plugins: [react()],
     build: {
       outDir: 'dist'
     }
   })
   ```

### Step 10: Contact Render Support

If none of the above works:
1. **Check Render status page:** https://status.render.com/
2. **Contact Render support** with your service URLs and error logs
3. **Check Render documentation:** https://render.com/docs

## Next Steps

1. **Check your Render dashboard** for the exact service URLs
2. **Test the health check endpoints** I added to the backend
3. **Use the updated test-connection.html** to test connectivity
4. **Set the correct environment variables**
5. **Redeploy both services**

Let me know what you find in your Render dashboard and I can help you with specific configuration issues! 