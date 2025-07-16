import os
from datetime import timedelta
from urllib.parse import quote_plus

class Config:
    """Configuration class for Flask application"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration - support for cloud databases
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # TEMPORARY FIX: Use PostgreSQL URL directly for immediate deployment
    # TODO: Remove this hardcoded URL once environment variables are working
    if not DATABASE_URL:
        DATABASE_URL = 'postgresql://prok_database_texr_user:UJ5uuxzIGYa37uWxoiDP3k1CacPQwKX3@dpg-d1rq0mvgi27c73cm8drg-a.oregon-postgres.render.com/prok_database_texr'
        print("🔧 TEMPORARY FIX: Using hardcoded PostgreSQL URL")
    
    # Use DATABASE_URL if available, otherwise fall back to SQLite
    if DATABASE_URL:
        # Handle Render's DATABASE_URL format
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        print(f"🔗 Using PostgreSQL database: {DATABASE_URL[:50]}...")
    else:
        # Fallback to SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///prok_db.sqlite'
        print("⚠️ No DATABASE_URL found, using SQLite (this won't work on Render!)")
    
    # Force PostgreSQL for production (Render)
    if os.environ.get('RENDER', 'false').lower() == 'true' or 'render.com' in os.environ.get('HOSTNAME', ''):
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required for production deployment on Render")
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        print("🚀 Production mode: Using PostgreSQL database")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ERROR_MESSAGE_KEY = 'error'
    JWT_BLACKLIST_ENABLED = False  # For simplicity, can be enabled later
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # Get allowed origins from environment variable
    ALLOWED_ORIGINS_ENV = os.environ.get('ALLOWED_ORIGINS')
    if ALLOWED_ORIGINS_ENV:
        CORS_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_ENV.split(',') if origin.strip()]
    else:
        # Default origins for development and production
        CORS_ORIGINS = [
            'https://prok-professional-networking-1-iv6a.onrender.com',
            'https://prok-frontend.onrender.com',
            'https://prok-professional-networking-se45.onrender.com',
            'https://prok-professional-networking-dvec.onrender.com',
            'https://prok-frontend-4h1s.onrender.com',
            'http://localhost:5173',
            'http://127.0.0.1:5173',
            'http://localhost:3000',
            'http://127.0.0.1:3000'
        ]
    
    # CORS methods and headers
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'X-Requested-With', 'Accept']
    CORS_EXPOSE_HEADERS = ['Content-Type', 'Authorization']
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_MAX_AGE = 3600
    
    # Rate limiting configuration
    RATELIMIT_STORAGE_URL = 'memory://'

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'avi', 'mov', 'wmv'}
    UPLOAD_URL_PREFIX = '/uploads/'
    
    # Production settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')