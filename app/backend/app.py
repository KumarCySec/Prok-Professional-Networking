from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from extensions import db, migrate, jwt
import os
import logging
import traceback
import sys

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    
    # Enable CORS - Place this RIGHT AFTER creating the Flask app
    CORS(app,
         origins="*",  # Allow all origins for debugging
         supports_credentials=False,  # Disable credentials for now
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
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        jwt.init_app(app)
        app.logger.info("✅ Extensions initialized successfully")
    except Exception as e:
        app.logger.error(f"❌ Failed to initialize extensions: {e}")
        app.logger.error(traceback.format_exc())
        raise
    
    # Import and register models after db is initialized
    try:
        with app.app_context():
            from models.user import User
            from models.profile import Profile  # Import profile model to avoid import errors
            app.logger.info("✅ Models imported successfully")
            
            # Initialize database tables
            try:
                db.create_all()
                app.logger.info("✅ Database tables created/verified")
            except Exception as db_error:
                app.logger.error(f"❌ Database table creation failed: {db_error}")
                app.logger.error(traceback.format_exc())
                # Don't raise here as migrations might handle this
    except Exception as e:
        app.logger.error(f"❌ Failed to import models: {e}")
        app.logger.error(traceback.format_exc())
        raise
    
    # Register blueprints
    try:
        from api.auth import auth_bp, init_limiter
        from api.profile import profile_bp
        from api.posts import posts_bp
        from api.feed import feed_bp
        from api.jobs import jobs_bp
        from api.messaging import messaging_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(profile_bp)
        app.register_blueprint(posts_bp)
        app.register_blueprint(feed_bp)
        app.register_blueprint(jobs_bp)
        app.register_blueprint(messaging_bp)
        app.logger.info("✅ Blueprints registered successfully")
    except Exception as e:
        app.logger.error(f"❌ Failed to register blueprints: {e}")
        app.logger.error(traceback.format_exc())
        raise
    
    # Initialize rate limiter
    try:
        init_limiter(app)
        app.logger.info("✅ Rate limiter initialized")
    except Exception as e:
        app.logger.error(f"❌ Failed to initialize rate limiter: {e}")
        # Don't raise here as rate limiting is not critical
    
    # Set up file serving for uploads
    from flask import send_from_directory
    
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serve uploaded files"""
        try:
            upload_folder = app.config['UPLOAD_FOLDER']
            return send_from_directory(upload_folder, filename)
        except Exception as e:
            app.logger.error(f"❌ File serving error: {e}")
            return jsonify({'error': 'File not found'}), 404
    
    @app.route('/')
    def health_check():
        """Health check endpoint"""
        try:
            return {'status': 'ok', 'message': 'Backend is running'}
        except Exception as e:
            app.logger.error(f"❌ Health check error: {e}")
            return {'status': 'error', 'message': 'Health check failed'}, 500
    
    @app.route('/api/health')
    def api_health():
        """API health check endpoint"""
        try:
            return {'status': 'ok', 'message': 'API is running'}
        except Exception as e:
            app.logger.error(f"❌ API health check error: {e}")
            return {'status': 'error', 'message': 'API health check failed'}, 500
    
    @app.route('/api/cors-test')
    def cors_test():
        """Test endpoint to verify CORS is working"""
        try:
            return {
                'status': 'ok', 
                'message': 'CORS test successful', 
                'origin': request.headers.get('Origin'),
                'cors_working': True
            }
        except Exception as e:
            app.logger.error(f"❌ CORS test error: {e}")
            return {'status': 'error', 'message': 'CORS test failed'}, 500
    
    @app.route('/api/cors-preflight', methods=['OPTIONS'])
    def cors_preflight():
        """Handle CORS preflight requests"""
        try:
            response = app.make_default_options_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept'
            response.headers['Access-Control-Allow-Credentials'] = 'false'
            response.headers['Access-Control-Max-Age'] = '3600'
            return response
        except Exception as e:
            app.logger.error(f"❌ CORS preflight error: {e}")
            return jsonify({'error': 'CORS preflight failed'}), 500
    
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
            app.logger.error(f"❌ Database test error: {e}")
            app.logger.error(traceback.format_exc())
            return {
                'status': 'error',
                'message': 'Database connection failed',
                'error': str(e)
            }, 500
    
    @app.route('/api/debug-config')
    def debug_config():
        """Debug endpoint to check configuration"""
        try:
            return {
                'status': 'ok',
                'database_url_set': bool(os.environ.get('DATABASE_URL')),
                'database_url_preview': os.environ.get('DATABASE_URL', 'Not set')[:50] + '...' if os.environ.get('DATABASE_URL') else 'Not set',
                'sqlalchemy_uri_preview': app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50] + '...' if app.config.get('SQLALCHEMY_DATABASE_URI') else 'Not set',
                'is_postgresql': 'postgresql://' in app.config.get('SQLALCHEMY_DATABASE_URI', ''),
                'is_sqlite': 'sqlite://' in app.config.get('SQLALCHEMY_DATABASE_URI', ''),
                'render_env': os.environ.get('RENDER', 'false'),
                'hostname': os.environ.get('HOSTNAME', 'Not set')
            }
        except Exception as e:
            app.logger.error(f"❌ Debug config error: {e}")
            return {
                'status': 'error',
                'message': 'Debug config failed',
                'error': str(e)
            }, 500
    
    def initialize_database():
        """Initialize database tables and run migrations"""
        try:
            with app.app_context():
                app.logger.info("🗄️ Initializing database...")
                app.logger.info(f"📊 Database URL: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')[:50]}...")
                
                # Test database connection first
                try:
                    from sqlalchemy import text
                    db.session.execute(text('SELECT 1'))
                    db.session.commit()
                    app.logger.info("✅ Database connection test successful")
                except Exception as conn_error:
                    app.logger.error(f"❌ Database connection failed: {conn_error}")
                    app.logger.error(traceback.format_exc())
                    raise
                
                # Create all tables
                try:
                    db.create_all()
                    app.logger.info("✅ Database tables created/verified")
                except Exception as table_error:
                    app.logger.error(f"❌ Table creation failed: {table_error}")
                    app.logger.error(traceback.format_exc())
                    raise
                
                # Run migrations if available
                try:
                    from flask_migrate import upgrade
                    upgrade()
                    app.logger.info("✅ Database migrations completed")
                except Exception as migration_error:
                    app.logger.warning(f"⚠️ Migration failed (this is normal for new databases): {migration_error}")
                
                # Test User model
                try:
                    user_count = User.query.count()
                    app.logger.info(f"✅ User model working. User count: {user_count}")
                except Exception as model_error:
                    app.logger.error(f"❌ User model test failed: {model_error}")
                    app.logger.error(traceback.format_exc())
                    raise
                
        except Exception as e:
            app.logger.error(f"❌ Database initialization failed: {e}")
            app.logger.error(traceback.format_exc())
            raise
    
    # Initialize database on startup
    try:
        initialize_database()
    except Exception as e:
        app.logger.error(f"❌ Failed to initialize database: {e}")
        # Don't raise here to allow the app to start even if DB init fails
    
    @app.route('/api/test-auth')
    @jwt_required()
    def test_auth():
        """Test endpoint to verify JWT authentication"""
        try:
            current_user_id = get_jwt_identity()
            return {'message': 'JWT working', 'user_id': current_user_id}
        except Exception as e:
            app.logger.error(f"❌ Auth test error: {e}")
            return jsonify({'error': 'Auth test failed'}), 500
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"404 error: {request.url}")
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 error: {error}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        app.logger.warning(f"405 error: {request.method} {request.url}")
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        app.logger.warning(f"413 error: File too large")
        return jsonify({'error': 'File too large'}), 413
    
    # Add a catch-all error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
