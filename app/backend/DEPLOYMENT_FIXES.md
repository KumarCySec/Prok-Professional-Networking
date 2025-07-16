# Deployment Fixes for Render

## Issues Fixed

### 1. Database Configuration
- **Problem**: App was hardcoded to use SQLite, which doesn't persist on Render's free tier
- **Solution**: Updated `config.py` to use `DATABASE_URL` environment variable from Render
- **Changes**: 
  - Added PostgreSQL support with `psycopg2-binary`
  - Updated database URL handling to support both PostgreSQL and SQLite
  - Added proper URL format conversion for Render's PostgreSQL

### 2. Database Initialization
- **Problem**: Database tables weren't being created on app startup
- **Solution**: Added automatic database initialization in `app.py`
- **Changes**:
  - Added `initialize_database()` function that runs on app startup
  - Creates tables with `db.create_all()`
  - Runs migrations with `flask_migrate upgrade`
  - Tests database connection

### 3. CORS Configuration
- **Problem**: CORS origins didn't include the correct frontend URL
- **Solution**: Updated CORS origins in `config.py` and `render.yaml`
- **Changes**:
  - Added `https://prok-professional-networking-dvec.onrender.com` to allowed origins
  - Updated `render.yaml` with correct frontend URL

### 4. Error Handling
- **Problem**: Generic error messages made debugging difficult
- **Solution**: Improved error handling in auth endpoints
- **Changes**:
  - Added specific database connection tests
  - Better error messages for different failure scenarios
  - Proper HTTP status codes (503 for database issues, 500 for server errors)

### 5. Build Process
- **Problem**: Build script didn't handle database setup
- **Solution**: Updated `build.sh` to create necessary directories
- **Changes**:
  - Added uploads directory creation
  - Better error handling and logging

## Deployment Steps

### 1. Update Render Environment Variables
Make sure these environment variables are set in your Render dashboard:

```
DATABASE_URL = [Your PostgreSQL database URL from Render]
SECRET_KEY = [Generated secret key]
JWT_SECRET_KEY = [Generated JWT secret key]
ALLOWED_ORIGINS = https://prok-professional-networking-dvec.onrender.com,https://prok-frontend.onrender.com,http://localhost:5173
FLASK_DEBUG = false
LOG_LEVEL = INFO
```

### 2. Create PostgreSQL Database
1. Go to your Render dashboard
2. Create a new PostgreSQL database service
3. Copy the database URL
4. Set it as the `DATABASE_URL` environment variable in your web service

### 3. Deploy the Backend
1. Push your changes to GitHub
2. Render will automatically rebuild and deploy
3. Check the build logs for any errors
4. Test the `/api/health` endpoint

### 4. Test Database Connection
After deployment, test the database connection:

```bash
# Test the health endpoint
curl https://your-backend-url.onrender.com/api/health

# Test database connection
curl https://your-backend-url.onrender.com/api/db-test
```

### 5. Test Authentication
Test the login and signup endpoints:

```bash
# Test signup
curl -X POST https://your-backend-url.onrender.com/api/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test123!"}'

# Test login
curl -X POST https://your-backend-url.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username_or_email":"testuser","password":"Test123!"}'
```

## Troubleshooting

### If you still get 503 errors:
1. Check if the PostgreSQL database is running
2. Verify the `DATABASE_URL` environment variable is set correctly
3. Check the application logs in Render dashboard
4. Test the database connection endpoint

### If you get 500 errors:
1. Check the application logs for specific error messages
2. Verify all required environment variables are set
3. Test the database connection manually

### If CORS errors persist:
1. Verify the frontend URL is in the `ALLOWED_ORIGINS` list
2. Check that the frontend is making requests to the correct backend URL
3. Test the CORS endpoint: `/api/cors-test`

## Files Modified

1. `config.py` - Database and CORS configuration
2. `app.py` - Database initialization and error handling
3. `api/auth.py` - Improved error handling in auth endpoints
4. `requirements.txt` - Added PostgreSQL support
5. `build.sh` - Enhanced build process
6. `render.yaml` - Updated environment variables
7. `test_db_connection.py` - Database testing script

## Testing Commands

```bash
# Test database connection locally
python test_db_connection.py

# Test the application locally
python app.py

# Test specific endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/db-test
``` 