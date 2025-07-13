from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from extensions import db, migrate, jwt
import os

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # CORS configuration for production
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173,https://your-frontend-url.onrender.com').split(',')
    
    CORS(app,
         origins=ALLOWED_ORIGINS,
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         supports_credentials=True,
         max_age=3600)
    
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
