import json
import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import RequestEntityTooLarge
from models.user import User
from models.profile import Profile
from utils import (
    validate_image_file, process_image, save_uploaded_file, 
    get_file_url, delete_file, validate_phone_number, 
    validate_website_url, sanitize_text
)
from extensions import db

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        # Convert string ID back to integer
        current_user_id = int(current_user_id)
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get or create profile
        profile = Profile.find_by_user_id(current_user_id)
        if not profile:
            profile = Profile(user_id=current_user_id)
            profile.save()
        
        # Combine user and profile data
        profile_data = user.to_dict()
        profile_data.update(profile.to_dict())
        
        # Parse JSON fields
        if profile_data.get('skills'):
            try:
                profile_data['skills'] = json.loads(profile_data['skills'])
            except json.JSONDecodeError:
                profile_data['skills'] = []
        
        if profile_data.get('education'):
            try:
                profile_data['education'] = json.loads(profile_data['education'])
            except json.JSONDecodeError:
                profile_data['education'] = []
        
        if profile_data.get('social_links'):
            try:
                profile_data['social_links'] = json.loads(profile_data['social_links'])
            except json.JSONDecodeError:
                profile_data['social_links'] = {}
        
        return jsonify({
            'success': True,
            'profile': profile_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting profile: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@profile_bp.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user's profile"""
    try:
        current_user_id = get_jwt_identity()
        # Convert string ID back to integer
        current_user_id = int(current_user_id)
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate and sanitize input data
        validation_errors = []
        
        # Basic text fields
        if 'first_name' in data:
            user.first_name = sanitize_text(data['first_name'], 50)
        
        if 'last_name' in data:
            user.last_name = sanitize_text(data['last_name'], 50)
        
        if 'bio' in data:
            user.bio = sanitize_text(data['bio'], 1000)
        
        if 'location' in data:
            user.location = sanitize_text(data['location'], 100)
        
        if 'company' in data:
            user.company = sanitize_text(data['company'], 100)
        
        if 'job_title' in data:
            user.job_title = sanitize_text(data['job_title'], 100)
        
        # Website validation
        if 'website' in data:
            valid, error = validate_website_url(data['website'])
            if not valid:
                validation_errors.append(error)
            else:
                user.website = data['website']
        
        # Phone validation
        if 'phone' in data:
            valid, error = validate_phone_number(data['phone'])
            if not valid:
                validation_errors.append(error)
            else:
                user.phone = data['phone']
        
        # Experience years validation
        if 'experience_years' in data:
            try:
                exp_years = int(data['experience_years'])
                if exp_years < 0 or exp_years > 50:
                    validation_errors.append("Experience years must be between 0 and 50")
                else:
                    user.experience_years = exp_years
            except (ValueError, TypeError):
                validation_errors.append("Experience years must be a valid number")
        
        # JSON fields validation
        if 'skills' in data:
            if isinstance(data['skills'], list):
                user.skills = json.dumps(data['skills'])
            else:
                validation_errors.append("Skills must be a list")
        
        if 'education' in data:
            if isinstance(data['education'], list):
                user.education = json.dumps(data['education'])
            else:
                validation_errors.append("Education must be a list")
        
        if 'social_links' in data:
            if isinstance(data['social_links'], dict):
                user.social_links = json.dumps(data['social_links'])
            else:
                validation_errors.append("Social links must be an object")
        
        # Return validation errors if any
        if validation_errors:
            return jsonify({
                'error': 'Validation errors',
                'details': validation_errors
            }), 400
        
        # Get or create profile
        profile = Profile.find_by_user_id(current_user_id)
        if not profile:
            profile = Profile(user_id=current_user_id)
        
        # Update profile-specific fields
        if 'headline' in data:
            profile.headline = sanitize_text(data['headline'], 200)
        
        if 'industry' in data:
            profile.industry = sanitize_text(data['industry'], 100)
        
        if 'current_position' in data:
            profile.current_position = sanitize_text(data['current_position'], 100)
        
        if 'company_size' in data:
            valid, error = profile.validate_company_size(data['company_size'])
            if not valid:
                validation_errors.append(error)
            else:
                profile.company_size = data['company_size']
        
        # Social media URLs
        if 'linkedin_url' in data:
            valid, error = profile.validate_url(data['linkedin_url'], 'linkedin')
            if not valid:
                validation_errors.append(error)
            else:
                profile.linkedin_url = data['linkedin_url']
        
        if 'twitter_url' in data:
            valid, error = profile.validate_url(data['twitter_url'], 'twitter')
            if not valid:
                validation_errors.append(error)
            else:
                profile.twitter_url = data['twitter_url']
        
        if 'github_url' in data:
            valid, error = profile.validate_url(data['github_url'], 'github')
            if not valid:
                validation_errors.append(error)
            else:
                profile.github_url = data['github_url']
        
        # Boolean fields
        if 'is_public' in data:
            profile.is_public = bool(data['is_public'])
        
        if 'allow_messages' in data:
            profile.allow_messages = bool(data['allow_messages'])
        
        if 'show_email' in data:
            profile.show_email = bool(data['show_email'])
        
        # Return validation errors if any
        if validation_errors:
            return jsonify({
                'error': 'Validation errors',
                'details': validation_errors
            }), 400
        
        # Save changes
        db.session.commit()
        
        # Return updated profile
        profile_data = user.to_dict()
        profile_data.update(profile.to_dict())
        
        # Parse JSON fields for response
        if profile_data.get('skills'):
            try:
                profile_data['skills'] = json.loads(profile_data['skills'])
            except json.JSONDecodeError:
                profile_data['skills'] = []
        
        if profile_data.get('education'):
            try:
                profile_data['education'] = json.loads(profile_data['education'])
            except json.JSONDecodeError:
                profile_data['education'] = []
        
        if profile_data.get('social_links'):
            try:
                profile_data['social_links'] = json.loads(profile_data['social_links'])
            except json.JSONDecodeError:
                profile_data['social_links'] = {}
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'profile': profile_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error updating profile: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@profile_bp.route('/api/profile/image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    """Upload profile image"""
    try:
        current_user_id = get_jwt_identity()
        # Convert string ID back to integer
        current_user_id = int(current_user_id)
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Validate image file
        valid, error = validate_image_file(file)
        if not valid:
            return jsonify({'error': error}), 400
        
        # Delete old profile image if exists
        if user.profile_image_url:
            old_filepath = user.profile_image_url.replace(current_app.config['UPLOAD_URL_PREFIX'], '')
            delete_file(old_filepath)
        
        # Process and save image
        try:
            # Process image (resize, optimize)
            processed_image = process_image(file)
            
            # Save to disk
            filepath = save_uploaded_file(processed_image, 'profile_images')
            
            # Generate URL
            image_url = get_file_url(filepath)
            
            # Update user profile
            user.profile_image_url = image_url
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Profile image uploaded successfully',
                'image_url': image_url
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Error processing image: {str(e)}")
            return jsonify({'error': 'Failed to process image'}), 500
        
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 5MB'}), 413
    except Exception as e:
        current_app.logger.error(f"Error uploading profile image: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@profile_bp.route('/api/profile/image', methods=['DELETE'])
@jwt_required()
def delete_profile_image():
    """Delete profile image"""
    try:
        current_user_id = get_jwt_identity()
        # Convert string ID back to integer
        current_user_id = int(current_user_id)
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.profile_image_url:
            return jsonify({'error': 'No profile image to delete'}), 404
        
        # Delete file from disk
        filepath = user.profile_image_url.replace(current_app.config['UPLOAD_URL_PREFIX'], '')
        delete_file(filepath)
        
        # Update user profile
        user.profile_image_url = None
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile image deleted successfully'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error deleting profile image: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@profile_bp.route('/api/profile/<int:user_id>', methods=['GET'])
def get_public_profile(user_id):
    """Get public profile by user ID"""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profile = Profile.find_by_user_id(user_id)
        if not profile or not profile.is_public:
            return jsonify({'error': 'Profile not found or not public'}), 404
        
        # Return public profile data only
        public_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'location': user.location,
            'company': user.company,
            'job_title': user.job_title,
            'profile_image_url': user.profile_image_url,
            'headline': profile.headline,
            'industry': profile.industry,
            'current_position': profile.current_position,
            'linkedin_url': profile.linkedin_url,
            'twitter_url': profile.twitter_url,
            'github_url': profile.github_url,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        
        # Parse JSON fields
        if user.skills:
            try:
                public_data['skills'] = json.loads(user.skills)
            except json.JSONDecodeError:
                public_data['skills'] = []
        
        if user.education:
            try:
                public_data['education'] = json.loads(user.education)
            except json.JSONDecodeError:
                public_data['education'] = []
        
        return jsonify({
            'success': True,
            'profile': public_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error getting public profile: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Routes will be implemented here 