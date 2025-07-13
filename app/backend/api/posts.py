import os
import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from sqlalchemy import desc, asc, func, or_, and_, text
from models.post import Post
from models.user import User
from extensions import db

posts_bp = Blueprint('posts', __name__)

# Simple in-memory cache for categories and popular tags
_cache: dict = {
    'categories': None,
    'popular_tags': None,
    'last_updated': None
}

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_media_file(file, folder='posts'):
    """Save uploaded media file and return the URL"""
    if file and file.filename:
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Create folder if it doesn't exist
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # Return URL
        return f"{current_app.config['UPLOAD_URL_PREFIX']}{folder}/{unique_filename}"
    return None

def invalidate_cache():
    """Invalidate cache when posts are modified"""
    _cache['categories'] = None
    _cache['popular_tags'] = None
    _cache['last_updated'] = None

@posts_bp.route('/api/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Create a new post"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get form data
        content = request.form.get('content', '').strip()
        rich_content = request.form.get('rich_content', '').strip()
        tags = request.form.get('tags', '')
        visibility = request.form.get('visibility', 'public')
        category = request.form.get('category', 'general')
        
        # Validate required fields
        if not content and not rich_content:
            return jsonify({'error': 'Post content is required'}), 400
        
        # Validate visibility
        if visibility not in ['public', 'connections', 'private']:
            return jsonify({'error': 'Invalid visibility setting'}), 400
        
        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            # Limit to 10 tags maximum
            tag_list = tag_list[:10]
        
        # Handle media upload
        media_url = None
        media_type = None
        
        if 'media' in request.files:
            file = request.files['media']
            if file and file.filename:
                # Validate file type
                allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
                if not allowed_file(file.filename, allowed_extensions):
                    return jsonify({'error': 'Invalid file type. Allowed: ' + ', '.join(allowed_extensions)}), 400
                
                # Determine media type
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    media_type = 'image'
                elif file_ext in ['mp4', 'avi', 'mov', 'wmv']:
                    media_type = 'video'
                else:
                    return jsonify({'error': 'Unsupported media type'}), 400
                
                # Save file
                media_url = save_media_file(file)
                if not media_url:
                    return jsonify({'error': 'Failed to save media file'}), 500
        
        # Create post
        post = Post(
            user_id=current_user_id,
            content=content,
            media_url=media_url,
            media_type=media_type,
            rich_content=rich_content,
            tags=tag_list,
            visibility=visibility,
            category=category
        )
        
        post.save()
        
        # Invalidate cache
        invalidate_cache()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': post.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating post: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@posts_bp.route('/api/posts', methods=['GET'])
@jwt_required()
def get_posts():
    """Get posts with advanced filtering and sorting"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        page = max(1, int(request.args.get('page', 1)))
        per_page = min(int(request.args.get('per_page', 20)), 50)  # Max 50 posts per page
        offset = (page - 1) * per_page
        
        # Filter parameters
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        visibility = request.args.get('visibility', '').strip()
        tags = request.args.get('tags', '').strip()
        user_id = request.args.get('user_id')
        
        # Sorting parameters
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Validate sort parameters
        allowed_sort_fields = ['created_at', 'likes_count', 'comments_count', 'views_count']
        if sort_by not in allowed_sort_fields:
            sort_by = 'created_at'
        
        if sort_order not in ['asc', 'desc']:
            sort_order = 'desc'
        
        # Build query
        query = Post.query.filter_by(is_active=True)
        
        # User filter
        if user_id:
            query = query.filter_by(user_id=int(user_id))
        else:
            # For feed posts, filter by visibility
            query = query.filter(Post.visibility.in_(['public', 'connections']))
        
        # Search filter
        if search:
            query = query.filter(
                Post.content.ilike(f'%{search}%')
            )
        
        # Category filter
        if category:
            query = query.filter(Post.category == category)
        
        # Visibility filter
        if visibility:
            query = query.filter(Post.visibility == visibility)
        
        # Tags filter
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag in tag_list:
                query = query.filter(Post.tags.ilike(f'%{tag}%'))
        
        # Apply sorting
        sort_field = getattr(Post, sort_by)
        if sort_order == 'desc':
            query = query.order_by(desc(sort_field))
        else:
            query = query.order_by(asc(sort_field))
        
        # Get total count for pagination
        total_count = query.count()
        
        # Apply pagination
        posts = query.limit(per_page).offset(offset).all()
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
        has_more = page < total_pages
        
        return jsonify({
            'posts': [post.to_dict() for post in posts],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_more': has_more
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching posts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@posts_bp.route('/api/posts/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all available post categories"""
    try:
        # Check cache first
        if _cache['categories'] and _cache['last_updated']:
            # Cache for 1 hour
            cache_age = datetime.utcnow() - _cache['last_updated']
            if cache_age.total_seconds() < 3600:
                return jsonify({'categories': _cache['categories']}), 200
        
        # Get categories from database
        categories = db.session.query(Post.category, func.count(Post.id).label('count'))\
            .filter_by(is_active=True)\
            .group_by(Post.category)\
            .order_by(desc('count'))\
            .all()
        
        category_list = [{'name': cat.category, 'count': cat.count} for cat in categories if cat.category]
        
        # Update cache
        _cache['categories'] = category_list
        _cache['last_updated'] = datetime.utcnow()
        
        return jsonify({'categories': category_list}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching categories: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@posts_bp.route('/api/posts/popular-tags', methods=['GET'])
@jwt_required()
def get_popular_tags():
    """Get most popular tags"""
    try:
        # Check cache first
        if _cache['popular_tags'] and _cache['last_updated']:
            # Cache for 1 hour
            cache_age = datetime.utcnow() - _cache['last_updated']
            if cache_age.total_seconds() < 3600:
                return jsonify({'tags': _cache['popular_tags']}), 200
        
        # Get all tags and count occurrences
        posts = Post.query.filter_by(is_active=True).all()
        tag_counts = {}
        
        for post in posts:
            if post.tags:
                try:
                    post_tags = json.loads(post.tags) if isinstance(post.tags, str) else post.tags
                    for tag in post_tags:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
                except (json.JSONDecodeError, TypeError):
                    continue
        
        # Sort by count and get top 20
        popular_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        tag_list = [{'name': tag, 'count': count} for tag, count in popular_tags]
        
        # Update cache
        _cache['popular_tags'] = tag_list
        _cache['last_updated'] = datetime.utcnow()
        
        return jsonify({'tags': tag_list}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching popular tags: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@posts_bp.route('/api/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    """Get a specific post by ID"""
    try:
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        return jsonify({'post': post.to_dict()}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching post {post_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@posts_bp.route('/api/posts/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Update a post"""
    try:
        current_user_id = get_jwt_identity()
        
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check if user owns the post
        if post.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get form data
        content = request.form.get('content', '').strip()
        rich_content = request.form.get('rich_content', '').strip()
        tags = request.form.get('tags', '')
        visibility = request.form.get('visibility')
        category = request.form.get('category')
        
        # Validate required fields
        if not content and not rich_content:
            return jsonify({'error': 'Post content is required'}), 400
        
        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        # Handle media upload
        media_url = post.media_url
        media_type = post.media_type
        
        if 'media' in request.files:
            file = request.files['media']
            if file and file.filename:
                # Validate file type
                allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
                if not allowed_file(file.filename, allowed_extensions):
                    return jsonify({'error': 'Invalid file type. Allowed: ' + ', '.join(allowed_extensions)}), 400
                
                # Determine media type
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    media_type = 'image'
                elif file_ext in ['mp4', 'avi', 'mov', 'wmv']:
                    media_type = 'video'
                else:
                    return jsonify({'error': 'Unsupported media type'}), 400
                
                # Save file
                media_url = save_media_file(file)
                if not media_url:
                    return jsonify({'error': 'Failed to save media file'}), 500
        
        # Update post
        update_data = {
            'content': content,
            'rich_content': rich_content,
            'tags': tag_list,
            'media_url': media_url,
            'media_type': media_type
        }
        
        if visibility:
            if visibility not in ['public', 'connections', 'private']:
                return jsonify({'error': 'Invalid visibility setting'}), 400
            update_data['visibility'] = visibility
        
        if category:
            update_data['category'] = category
        
        post.update(**update_data)
        
        # Invalidate cache
        invalidate_cache()
        
        return jsonify({
            'message': 'Post updated successfully',
            'post': post.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error updating post {post_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@posts_bp.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete a post"""
    try:
        current_user_id = get_jwt_identity()
        
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Check if user owns the post
        if post.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        post.delete()
        
        # Invalidate cache
        invalidate_cache()
        
        return jsonify({'message': 'Post deleted successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error deleting post {post_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@posts_bp.route('/api/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    """Like/unlike a post"""
    try:
        current_user_id = get_jwt_identity()
        
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # TODO: Implement like/unlike logic with a separate Like model
        # For now, just increment likes
        post.increment_likes()
        
        return jsonify({
            'message': 'Post liked successfully',
            'likes_count': post.likes_count
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error liking post {post_id}: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 