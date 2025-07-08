import re
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from extensions import db

class User(db.Model):
    """User model with authentication and validation"""
    __tablename__ = 'users'
    
    # Database columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Profile fields (added by migration)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_image_url = db.Column(db.String(500), nullable=True)
    skills = db.Column(db.Text, nullable=True)  # JSON string
    experience_years = db.Column(db.Integer, nullable=True)
    education = db.Column(db.Text, nullable=True)  # JSON string
    social_links = db.Column(db.Text, nullable=True)  # JSON string
    
    def __init__(self, username, email, password):
        """Initialize user with validation"""
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Set password with validation and hashing"""
        if not self._validate_password(password):
            raise ValueError("Password does not meet complexity requirements")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def _validate_password(self, password):
        """Validate password complexity requirements"""
        if len(password) < 8:
            return False
        
        # Check for uppercase, lowercase, digit, and special character
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        
        return all([has_upper, has_lower, has_digit, has_special])
    
    def _validate_username(self, username):
        """Validate username format"""
        if len(username) < 3 or len(username) > 80:
            return False
        # Username should be alphanumeric with underscores and hyphens
        return re.match(r'^[a-zA-Z0-9_-]+$', username) is not None
    
    def _validate_email(self, email):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def save(self):
        """Save user to database with validation"""
        # Validate username and email
        if not self._validate_username(self.username):
            raise ValueError("Invalid username format")
        
        if not self._validate_email(self.email):
            raise ValueError("Invalid email format")
        
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Username or email already exists")
    
    def to_dict(self):
        """Convert user to dictionary (excluding sensitive data)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'bio': self.bio,
            'location': self.location,
            'company': self.company,
            'job_title': self.job_title,
            'website': self.website,
            'phone': self.phone,
            'profile_image_url': self.profile_image_url,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'education': self.education,
            'social_links': self.social_links,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    @classmethod
    def find_by_username(cls, username):
        """Find user by username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID"""
        return cls.query.get(user_id)
    
    def __repr__(self):
        return f'<User {self.username}>'
