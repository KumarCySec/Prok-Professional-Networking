import os
from datetime import timedelta
from urllib.parse import quote_plus

class Config:
    """Configuration class for Flask application"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration - support for cloud databases
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Default password is URL-encoded to handle special characters like @
    default_password = quote_plus('Kumar@249')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or f'mysql://root:{default_password}@localhost/prok_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # Get allowed origins from environment variable
    ALLOWED_ORIGINS_ENV = os.environ.get('ALLOWED_ORIGINS')
    if ALLOWED_ORIGINS_ENV:
        CORS_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_ENV.split(',') if origin.strip()]
    else:
        # Default origins for development
        CORS_ORIGINS = [
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