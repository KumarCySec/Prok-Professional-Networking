from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Import and register models after db is initialized
    with app.app_context():
        from models.user import User
        from models.profile import Profile  # Import profile model to avoid import errors
    
    # Register blueprints
    from api.auth import auth_bp, init_limiter
    app.register_blueprint(auth_bp)
    
    # Initialize rate limiter
    init_limiter(app)
    
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
