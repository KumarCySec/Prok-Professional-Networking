from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from extensions import db, migrate, jwt
import os
import logging

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # CORS configuration for production - MUST be before registering blueprints
    # Get allowed origins from environment variable
    allowed_origins_env = os.getenv('ALLOWED_ORIGINS')
    
    if allowed_origins_env:
        # Split by comma and strip whitespace
        ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins_env.split(',') if origin.strip()]
        app.logger.info(f"CORS configured with origins: {ALLOWED_ORIGINS}")
    else:
        # Use default origins from config
        ALLOWED_ORIGINS = app.config.get('CORS_ORIGINS', [
            'http://localhost:5173',
            'http://127.0.0.1:5173',
            'http://localhost:3000',
            'http://127.0.0.1:3000'
        ])
        app.logger.warning("ALLOWED_ORIGINS not set, using default development origins")
    
    # Initialize CORS with proper configuration
    CORS(app,
         origins=ALLOWED_ORIGINS,
         methods=app.config.get('CORS_METHODS', ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH']),
         allow_headers=app.config.get('CORS_ALLOW_HEADERS', ['Content-Type', 'Authorization', 'X-Requested-With', 'Accept']),
         expose_headers=app.config.get('CORS_EXPOSE_HEADERS', ['Content-Type', 'Authorization']),
         supports_credentials=app.config.get('CORS_SUPPORTS_CREDENTIALS', True),
         max_age=app.config.get('CORS_MAX_AGE', 3600))
    
    app.logger.info("CORS initialized successfully")
    
    # Import and register models after db is initialized
    with app.app_context():
        from models.user import User
        from models.profile import Profile  # Import profile model to avoid import errors
    
    # Register blueprints AFTER CORS is configured
    from api.auth import auth_bp, init_limiter
    from api.profile import profile_bp
    from api.posts import posts_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(posts_bp)
    
    # Initialize rate limiter
    init_limiter(app)
    
    # Set up file serving for uploads
    from flask import send_from_directory
    
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serve uploaded files"""
        upload_folder = app.config['UPLOAD_FOLDER']
        return send_from_directory(upload_folder, filename)
    
    @app.route('/')
    def health_check():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Backend is running'}
    
    @app.route('/api/health')
    def api_health():
        """API health check endpoint"""
        return {'status': 'ok', 'message': 'API is running'}
    
    @app.route('/api/cors-test')
    def cors_test():
        """Test endpoint to verify CORS is working"""
        return {'status': 'ok', 'message': 'CORS test successful', 'origin': request.headers.get('Origin')}
    
    @app.route('/api/test-auth')
    @jwt_required()
    def test_auth():
        """Test endpoint to verify JWT authentication"""
        current_user_id = get_jwt_identity()
        return {'message': 'JWT working', 'user_id': current_user_id}
    
    return app

# Create app instance for CLI commands (lazy initialization)
app = None

def get_app():
    """Get or create the Flask app instance"""
    global app
    if app is None:
        app = create_app()
    return app

# For Flask CLI compatibility - this is what Flask looks for
app = get_app()

if __name__ == '__main__':
    app.run(debug=True)
