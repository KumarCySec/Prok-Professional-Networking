from flask import Blueprint, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import re
import traceback
from datetime import timedelta
from extensions import db
from models.user import User

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__)

def init_limiter(app):
    """Initialize rate limiter with the Flask app"""
    try:
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"]
        )
        return limiter
    except Exception as e:
        current_app.logger.error(f"❌ Failed to initialize rate limiter: {e}")
        return None

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks"""
    if not text:
        return ""
    # Remove potentially dangerous characters
    return re.sub(r'[<>"\']', '', str(text).strip())

def validate_password_complexity(password):
    """Validate password meets complexity requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long" 
    
    # Check for uppercase, lowercase, digit, and special character
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    
    if not all([has_upper, has_lower, has_digit, has_special]):
        return False, "Password must contain uppercase, lowercase, digit, and special character"
    
    return True, "Password is valid"

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    """Registration endpoint - Allow new users to register"""
    try:
        current_app.logger.info("📝 Signup request received")
        
        # Get and sanitize input data
        data = request.get_json()
        if not data:
            current_app.logger.warning("❌ Signup: No data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        username = sanitize_input(data.get('username'))
        email = sanitize_input(data.get('email'))
        password = data.get('password')  # Don't sanitize password as it may contain special chars
        
        current_app.logger.info(f"📝 Signup attempt for username: {username}, email: {email}")
        
        # Validate required fields
        if not username or not email or not password:
            current_app.logger.warning("❌ Signup: Missing required fields")
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Validate username format
        if len(username) < 3 or len(username) > 80:
            current_app.logger.warning(f"❌ Signup: Invalid username length: {username}")
            return jsonify({'error': 'Username must be between 3 and 80 characters'}), 400
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            current_app.logger.warning(f"❌ Signup: Invalid username format: {username}")
            return jsonify({'error': 'Username can only contain letters, numbers, underscores, and hyphens'}), 400
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            current_app.logger.warning(f"❌ Signup: Invalid email format: {email}")
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password complexity
        is_valid, password_message = validate_password_complexity(password)
        if not is_valid:
            current_app.logger.warning(f"❌ Signup: Password complexity failed: {password_message}")
            return jsonify({'error': password_message}), 400
        
        # Check if user already exists
        existing_user = User.find_by_username(username)
        if existing_user:
            current_app.logger.warning(f"❌ Signup: Username already exists: {username}")
            return jsonify({'error': 'Username already exists'}), 400
        
        existing_email = User.find_by_email(email)
        if existing_email:
            current_app.logger.warning(f"❌ Signup: Email already exists: {email}")
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        new_user = User(username=username, email=email, password=password)
        
        # Save user to database
        try:
            new_user.save()
            current_app.logger.info(f"✅ Signup successful for user: {username}")
        except ValueError as e:
            current_app.logger.error(f"❌ Signup save error: {e}")
            return jsonify({'error': str(e)}), 400
        
        # Generate JWT token
        access_token = create_access_token(
            identity=str(new_user.id),
            expires_delta=timedelta(hours=24)
        )
        
        # Return success response
        return jsonify({
            'message': 'User created successfully',
            'user': new_user.to_dict(),
            'access_token': access_token
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"❌ Signup unexpected error: {e}")
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Login endpoint - Authenticate users and issue JWT token"""
    try:
        current_app.logger.info("🔐 Login request received")
        
        # Get and sanitize input data
        data = request.get_json()
        if not data:
            current_app.logger.warning("❌ Login: No data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        username_or_email = sanitize_input(data.get('username_or_email'))
        password = data.get('password')
        
        current_app.logger.info(f"🔐 Login attempt for: {username_or_email}")
        
        # Validate required fields
        if not username_or_email or not password:
            current_app.logger.warning("❌ Login: Missing required fields")
            return jsonify({'error': 'Username/email and password are required'}), 400
        
        # Check database connection first
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db.session.commit()
        except Exception as db_error:
            current_app.logger.error(f"❌ Database connection failed: {db_error}")
            return jsonify({'error': 'Database connection error. Please try again later.'}), 503
        
        # Find user by username or email
        user = None
        try:
            if '@' in username_or_email:
                # Try to find by email
                user = User.find_by_email(username_or_email)
                current_app.logger.info(f"🔍 Searching by email: {username_or_email}")
            else:
                # Try to find by username
                user = User.find_by_username(username_or_email)
                current_app.logger.info(f"🔍 Searching by username: {username_or_email}")
        except Exception as query_error:
            current_app.logger.error(f"❌ Database query error: {query_error}")
            return jsonify({'error': 'Database error. Please try again later.'}), 503
        
        # Check if user exists and password is correct
        if not user:
            current_app.logger.warning(f"❌ Login: User not found: {username_or_email}")
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        if not user.check_password(password):
            current_app.logger.warning(f"❌ Login: Invalid password for user: {username_or_email}")
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            current_app.logger.warning(f"❌ Login: Inactive account: {username_or_email}")
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Generate JWT token
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=24)
        )
        
        current_app.logger.info(f"✅ Login successful for user: {username_or_email}")
        
        # Return success response
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"❌ Login unexpected error: {e}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error. Please try again later.'}), 500

@auth_bp.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = get_jwt_identity()
        current_app.logger.info(f"👤 Getting current user: {current_user_id}")
        
        user = User.find_by_id(current_user_id)
        
        if not user:
            current_app.logger.warning(f"❌ User not found: {current_user_id}")
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"❌ Get current user error: {e}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout endpoint (client-side token removal)"""
    try:
        current_user_id = get_jwt_identity()
        current_app.logger.info(f"🚪 Logout for user: {current_user_id}")
        
        # JWT tokens are stateless, so logout is handled client-side
        # In a production environment, you might want to implement a blacklist
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        current_app.logger.error(f"❌ Logout error: {e}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': 'Internal server error'}), 500
