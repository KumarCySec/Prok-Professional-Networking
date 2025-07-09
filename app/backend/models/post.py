import json
from datetime import datetime
from extensions import db

class Post(db.Model):
    """Post model for user-generated content"""
    __tablename__ = 'posts'
    
    # Database columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(500), nullable=True)
    media_type = db.Column(db.String(20), nullable=True)  # 'image', 'video'
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Rich text content (for formatted posts)
    rich_content = db.Column(db.Text, nullable=True)
    
    # Post metadata
    tags = db.Column(db.Text, nullable=True)  # JSON string of tags
    visibility = db.Column(db.String(20), default='public')  # 'public', 'connections', 'private'
    
    # Relationships
    user = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    
    def __init__(self, user_id, content, media_url=None, media_type=None, rich_content=None, tags=None, visibility='public'):
        """Initialize post with validation"""
        self.user_id = user_id
        self.content = content
        self.media_url = media_url
        self.media_type = media_type
        self.rich_content = rich_content
        self.tags = json.dumps(tags) if tags else None
        self.visibility = visibility
    
    def save(self):
        """Save post to database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to save post: {str(e)}")
    
    def update(self, **kwargs):
        """Update post fields"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == 'tags' and value is not None:
                    setattr(self, key, json.dumps(value))
                else:
                    setattr(self, key, value)
        
        self.updated_at = datetime.utcnow()
        return self.save()
    
    def delete(self):
        """Soft delete post"""
        self.is_active = False
        return self.save()
    
    def to_dict(self):
        """Convert post to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'rich_content': self.rich_content,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'tags': json.loads(self.tags) if self.tags else [],
            'visibility': self.visibility,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'profile_image_url': self.user.profile_image_url
            } if self.user else None
        }
    
    @classmethod
    def find_by_id(cls, post_id):
        """Find post by ID"""
        return cls.query.filter_by(id=post_id, is_active=True).first()
    
    @classmethod
    def find_by_user(cls, user_id, limit=20, offset=0):
        """Find posts by user ID"""
        return cls.query.filter_by(user_id=user_id, is_active=True)\
                       .order_by(cls.created_at.desc())\
                       .limit(limit)\
                       .offset(offset)\
                       .all()
    
    @classmethod
    def get_feed_posts(cls, user_id=None, limit=20, offset=0):
        """Get posts for feed (public posts or from connections)"""
        query = cls.query.filter_by(is_active=True)
        
        if user_id:
            # For now, return all public posts
            # TODO: Implement connection-based filtering
            query = query.filter(cls.visibility.in_(['public', 'connections']))
        
        return query.order_by(cls.created_at.desc())\
                   .limit(limit)\
                   .offset(offset)\
                   .all()
    
    def increment_likes(self):
        """Increment likes count"""
        self.likes_count += 1
        db.session.commit()
    
    def decrement_likes(self):
        """Decrement likes count"""
        if self.likes_count > 0:
            self.likes_count -= 1
            db.session.commit()
    
    def increment_comments(self):
        """Increment comments count"""
        self.comments_count += 1
        db.session.commit()
    
    def decrement_comments(self):
        """Decrement comments count"""
        if self.comments_count > 0:
            self.comments_count -= 1
            db.session.commit()
    
    def __repr__(self):
        return f'<Post {self.id} by User {self.user_id}>'
