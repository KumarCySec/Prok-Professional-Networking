from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from extensions import db, migrate, jwt
import os
import logging

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    
    # Enable CORS - Place this RIGHT AFTER creating the Flask app
    CORS(app,
         origins=[
             "https://prok-professional-networking-1-iv6a.onrender.com",
             "http://localhost:5173",
             "http://127.0.0.1:5173",
             "http://localhost:3000",
             "http://127.0.0.1:3000"
         ],
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
         expose_headers=["Content-Type", "Authorization"])
    
    app.config.from_object(config_class)
    
    # Session configuration for cross-origin requests
    app.config['SESSION_COOKIE_SAMESITE'] = "None"
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = False  # Allow JavaScript access for SPA
    app.config['SESSION_COOKIE_DOMAIN'] = None  # Let browser handle domain
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Import and register models after db is initialized
    with app.app_context():
        from models.user import User
        from models.profile import Profile  # Import profile model to avoid import errors
    
    # Register blueprints
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
        return {
            'status': 'ok', 
            'message': 'CORS test successful', 
            'origin': request.headers.get('Origin'),
            'cors_working': True
        }
    
    @app.route('/api/cors-preflight', methods=['OPTIONS'])
    def cors_preflight():
        """Handle CORS preflight requests"""
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '3600'
        return response
    
    @app.route('/api/db-test')
    def db_test():
        """Test endpoint to verify database connection"""
        try:
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            
            # Test User model
            user_count = User.query.count()
            
            return {
                'status': 'ok',
                'message': 'Database connection successful',
                'user_count': user_count,
                'database_url': app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50] + '...' if app.config.get('SQLALCHEMY_DATABASE_URI') else 'Not set'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': 'Database connection failed',
                'error': str(e)
            }, 500
    
    @app.route('/api/test-auth')
    @jwt_required()
    def test_auth():
        """Test endpoint to verify JWT authentication"""
        current_user_id = get_jwt_identity()
        return {'message': 'JWT working', 'user_id': current_user_id}
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'error': 'File too large'}), 413
    
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
