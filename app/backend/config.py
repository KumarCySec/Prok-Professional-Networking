import os
from datetime import timedelta
from urllib.parse import quote_plus

class Config:
    """Configuration class for Flask application"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration - URL encode the password to handle special characters
    # Default password is URL-encoded to handle special characters like @
    default_password = quote_plus('Kumar@249')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'mysql://root:{default_password}@localhost/prok_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # CORS configuration
    CORS_HEADERS = 'Content-Type'
    
    # Rate limiting configuration
    RATELIMIT_STORAGE_URL = 'memory://'
