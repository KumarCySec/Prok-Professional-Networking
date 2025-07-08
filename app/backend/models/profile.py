# Profile model placeholder
# This will be implemented later with full profile functionality
import json
import re
from datetime import datetime
from extensions import db

class Profile(db.Model):
    """Profile model with comprehensive profile functionality"""
    __tablename__ = 'profiles'
    
    # Basic profile fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Professional information
    headline = db.Column(db.String(200), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    current_position = db.Column(db.String(100), nullable=True)
    company_size = db.Column(db.String(50), nullable=True)  # e.g., "1-10", "11-50", "51-200"
    
    # Contact information
    linkedin_url = db.Column(db.String(200), nullable=True)
    twitter_url = db.Column(db.String(200), nullable=True)
    github_url = db.Column(db.String(200), nullable=True)
    
    # Preferences
    is_public = db.Column(db.Boolean, default=True)
    allow_messages = db.Column(db.Boolean, default=True)
    show_email = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, **kwargs):
        """Initialize profile with validation"""
        self.user_id = user_id
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def validate_headline(self, headline):
        """Validate headline length and content"""
        if headline and len(headline) > 200:
            return False, "Headline must be 200 characters or less"
        return True, None
    
    def validate_url(self, url, platform):
        """Validate URL format for social platforms"""
        if not url:
            return True, None
        
        # Basic URL validation
        url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        if not re.match(url_pattern, url):
            return False, f"Invalid {platform} URL format"
        
        # Platform-specific validation
        if platform == 'linkedin' and 'linkedin.com' not in url:
            return False, "Invalid LinkedIn URL"
        elif platform == 'twitter' and 'twitter.com' not in url and 'x.com' not in url:
            return False, "Invalid Twitter/X URL"
        elif platform == 'github' and 'github.com' not in url:
            return False, "Invalid GitHub URL"
        
        return True, None
    
    def validate_company_size(self, size):
        """Validate company size format"""
        if not size:
            return True, None
        
        valid_sizes = ['1-10', '11-50', '51-200', '201-500', '501-1000', '1000+']
        if size not in valid_sizes:
            return False, "Invalid company size. Must be one of: " + ", ".join(valid_sizes)
        
        return True, None
    
    def save(self):
        """Save profile to database with validation"""
        # Validate fields
        valid, error = self.validate_headline(self.headline)
        if not valid:
            raise ValueError(error)
        
        valid, error = self.validate_url(self.linkedin_url, 'linkedin')
        if not valid:
            raise ValueError(error)
        
        valid, error = self.validate_url(self.twitter_url, 'twitter')
        if not valid:
            raise ValueError(error)
        
        valid, error = self.validate_url(self.github_url, 'github')
        if not valid:
            raise ValueError(error)
        
        valid, error = self.validate_company_size(self.company_size)
        if not valid:
            raise ValueError(error)
        
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to save profile: {str(e)}")
    
    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'headline': self.headline,
            'industry': self.industry,
            'current_position': self.current_position,
            'company_size': self.company_size,
            'linkedin_url': self.linkedin_url,
            'twitter_url': self.twitter_url,
            'github_url': self.github_url,
            'is_public': self.is_public,
            'allow_messages': self.allow_messages,
            'show_email': self.show_email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Find profile by user ID"""
        return cls.query.filter_by(user_id=user_id).first()
    
    def __repr__(self):
        return f'<Profile {self.id} for User {self.user_id}>'
