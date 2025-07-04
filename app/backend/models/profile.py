# Profile model placeholder
# This will be implemented later with full profile functionality
from extensions import db

class Profile(db.Model):
    """Profile model placeholder - will be expanded later"""
    __tablename__ = 'profiles'
    
    # Basic profile fields
    id = db.Column(db.Integer, primary_key=True)
    # Add more profile fields here when needed
    
    def __repr__(self):
        return f'<Profile {self.id}>'
