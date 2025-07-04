from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import timedelta
from extensions import db
from models.user import User

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__)

def init_limiter(app):
    """Initialize rate limiter with the Flask app"""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    return limiter

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
        # Get and sanitize input data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = sanitize_input(data.get('username'))
        email = sanitize_input(data.get('email'))
        password = data.get('password')  # Don't sanitize password as it may contain special chars
        
        # Validate required fields
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Validate username format
        if len(username) < 3 or len(username) > 80:
            return jsonify({'error': 'Username must be between 3 and 80 characters'}), 400
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return jsonify({'error': 'Username can only contain letters, numbers, underscores, and hyphens'}), 400
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password complexity
        is_valid, password_message = validate_password_complexity(password)
        if not is_valid:
            return jsonify({'error': password_message}), 400
        
        # Check if user already exists
        existing_user = User.find_by_username(username)
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        existing_email = User.find_by_email(email)
        if existing_email:
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        new_user = User(username=username, email=email, password=password)
        
        # Save user to database
        try:
            new_user.save()
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        # Generate JWT token
        access_token = create_access_token(
            identity=new_user.id,
            expires_delta=timedelta(hours=24)
        )
        
        # Return success response
        return jsonify({
            'message': 'User created successfully',
            'user': new_user.to_dict(),
            'access_token': access_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Login endpoint - Authenticate users and issue JWT token"""
    try:
        # Get and sanitize input data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username_or_email = sanitize_input(data.get('username_or_email'))
        password = data.get('password')
        
        # Validate required fields
        if not username_or_email or not password:
            return jsonify({'error': 'Username/email and password are required'}), 400
        
        # Find user by username or email
        user = None
        if '@' in username_or_email:
            # Try to find by email
            user = User.find_by_email(username_or_email)
        else:
            # Try to find by username
            user = User.find_by_username(username_or_email)
        
        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username/email or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Generate JWT token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=24)
        )
        
        # Return success response
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout endpoint (client-side token removal)"""
    # JWT tokens are stateless, so logout is handled client-side
    # In a production environment, you might want to implement a blacklist
    return jsonify({'message': 'Logout successful'}), 200
