import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models.post import Post
from models.user import User
from extensions import db

posts_bp = Blueprint('posts', __name__)

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
            visibility=visibility
        )
        
        post.save()
        
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
    """Get posts for feed"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get query parameters
        limit = min(int(request.args.get('limit', 20)), 50)  # Max 50 posts
        offset = int(request.args.get('offset', 0))
        user_id = request.args.get('user_id')
        
        if user_id:
            # Get posts by specific user
            posts = Post.find_by_user(int(user_id), limit=limit, offset=offset)
        else:
            # Get feed posts
            posts = Post.get_feed_posts(user_id=current_user_id, limit=limit, offset=offset)
        
        return jsonify({
            'posts': [post.to_dict() for post in posts],
            'count': len(posts),
            'has_more': len(posts) == limit
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching posts: {str(e)}")
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
        
        post.update(**update_data)
        
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