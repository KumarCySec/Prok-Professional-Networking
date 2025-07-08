import os
import uuid
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import io
from flask import current_app
import re

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def validate_file_size(file):
    """Validate file size"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset file pointer
    
    max_size = current_app.config['MAX_CONTENT_LENGTH']
    if size > max_size:
        return False, f"File size exceeds maximum limit of {max_size // (1024*1024)}MB"
    
    return True, None

def validate_image_file(file):
    """Validate image file type and content"""
    # Check file extension
    if not allowed_file(file.filename):
        return False, "File type not allowed. Please upload PNG, JPG, JPEG, GIF, or WebP files."
    
    # Check file size
    valid, error = validate_file_size(file)
    if not valid:
        return False, error
    
    # Validate image content
    try:
        file.seek(0)
        image = Image.open(file)
        image.verify()  # Verify it's actually an image
        file.seek(0)  # Reset file pointer
        return True, None
    except Exception as e:
        return False, "Invalid image file. Please upload a valid image."

def generate_unique_filename(original_filename):
    """Generate unique filename with timestamp and UUID"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    extension = original_filename.rsplit('.', 1)[1].lower()
    
    return f"{timestamp}_{unique_id}.{extension}"

def process_image(image_file, max_size=(800, 800), quality=85):
    """Process and optimize image"""
    try:
        # Open image
        image = Image.open(image_file)
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparent images
            background = Image.new('RGB', image.size)
            background.paste((255, 255, 255), (0, 0, image.size[0], image.size[1]))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Resize if larger than max_size
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized image to bytes
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output
    except Exception as e:
        raise ValueError(f"Failed to process image: {str(e)}")

def save_uploaded_file(file, subfolder=''):
    """Save uploaded file to disk"""
    # Ensure upload directory exists
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if subfolder:
        upload_folder = os.path.join(upload_folder, subfolder)
    
    os.makedirs(upload_folder, exist_ok=True)
    
    # Generate unique filename
    filename = generate_unique_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    
    # Save file
    file.save(filepath)
    
    # Return relative path for URL generation
    relative_path = os.path.join(subfolder, filename) if subfolder else filename
    return relative_path

def get_file_url(filepath):
    """Generate URL for uploaded file"""
    return current_app.config['UPLOAD_URL_PREFIX'] + filepath

def delete_file(filepath):
    """Delete file from disk"""
    try:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception as e:
        print(f"Error deleting file {filepath}: {str(e)}")
        return False

def validate_phone_number(phone):
    """Validate phone number format"""
    if not phone:
        return True, None
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it's a valid length (7-15 digits)
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False, "Phone number must be between 7 and 15 digits"
    
    return True, None

def validate_website_url(url):
    """Validate website URL format"""
    if not url:
        return True, None
    
    # Basic URL validation
    url_pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
    if not re.match(url_pattern, url):
        return False, "Invalid website URL format"
    
    return True, None

def sanitize_text(text, max_length=None):
    """Sanitize text input"""
    if not text:
        return text
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip() 