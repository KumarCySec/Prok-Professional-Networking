# Profile Data Management Implementation

This document outlines the complete implementation of the Profile Data Management system with image upload functionality for the Prok Professional Networking platform.

## Overview

The Profile Data Management system provides comprehensive user profile functionality including:
- Extended user profile fields
- Image upload and processing
- Profile validation and security
- Frontend integration
- Public profile viewing

## Backend Implementation

### 1. Database Models

#### Extended User Model (`models/user.py`)
Added profile-related fields to the existing User model:

```python
# Profile-related fields
first_name = db.Column(db.String(50), nullable=True)
last_name = db.Column(db.String(50), nullable=True)
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
```

#### Profile Model (`models/profile.py`)
New comprehensive Profile model with validation:

```python
class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Professional information
    headline = db.Column(db.String(200), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    current_position = db.Column(db.String(100), nullable=True)
    company_size = db.Column(db.String(50), nullable=True)
    
    # Social media links
    linkedin_url = db.Column(db.String(200), nullable=True)
    twitter_url = db.Column(db.String(200), nullable=True)
    github_url = db.Column(db.String(200), nullable=True)
    
    # Privacy settings
    is_public = db.Column(db.Boolean, default=True)
    allow_messages = db.Column(db.Boolean, default=True)
    show_email = db.Column(db.Boolean, default=False)
```

### 2. File Upload System

#### Configuration (`config.py`)
Added file upload configuration:

```python
# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_URL_PREFIX = '/uploads/'
```

#### Utility Functions (`utils.py`)
Comprehensive file handling utilities:

- `validate_image_file()`: Validates file type, size, and content
- `process_image()`: Resizes, optimizes, and converts images
- `save_uploaded_file()`: Securely saves files with unique names
- `get_file_url()`: Generates public URLs for uploaded files
- `delete_file()`: Safely removes files from disk

### 3. API Endpoints

#### Profile Management (`api/profile.py`)

**GET /api/profile**
- Returns current user's complete profile
- Automatically creates profile if it doesn't exist
- Parses JSON fields (skills, education, social_links)

**PUT /api/profile**
- Updates user profile with validation
- Supports partial updates
- Validates all input fields
- Returns updated profile data

**POST /api/profile/image**
- Handles profile image upload
- Validates file type and size
- Processes and optimizes images
- Updates user's profile_image_url

**DELETE /api/profile/image**
- Removes profile image
- Deletes file from disk
- Clears profile_image_url

**GET /api/profile/<user_id>**
- Returns public profile by user ID
- Respects privacy settings
- Returns only public information

### 4. Security Features

#### File Validation
- File type validation (PNG, JPG, JPEG, GIF, WebP)
- File size limits (5MB maximum)
- Image content validation
- Secure file naming with timestamps and UUIDs

#### Input Validation
- Text field length limits
- URL format validation
- Phone number validation
- JSON field validation
- XSS prevention through text sanitization

#### Access Control
- JWT authentication required for all profile operations
- Public profile access respects privacy settings
- Secure file serving with proper headers

## Frontend Implementation

### 1. API Integration (`components/profile/api.ts`)

#### TypeScript Interfaces
```typescript
export interface ProfileData {
  id?: number;
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  bio?: string;
  location?: string;
  company?: string;
  job_title?: string;
  website?: string;
  phone?: string;
  profile_image_url?: string;
  skills?: string[];
  experience_years?: number;
  education?: any[];
  social_links?: Record<string, string>;
  headline?: string;
  industry?: string;
  current_position?: string;
  company_size?: string;
  linkedin_url?: string;
  twitter_url?: string;
  github_url?: string;
  is_public?: boolean;
  allow_messages?: boolean;
  show_email?: boolean;
}
```

#### API Functions
- `getProfile()`: Fetch current user's profile
- `updateProfile()`: Update profile with validation
- `uploadProfileImage()`: Upload and process profile image
- `deleteProfileImage()`: Remove profile image
- `getPublicProfile()`: Fetch public profile by user ID
- `validateProfileData()`: Client-side validation
- `formatProfileData()`: Format data for display

### 2. Error Handling
- Comprehensive error handling for all API calls
- User-friendly error messages
- Validation error details
- Network error handling

## Database Migration

### Simple Migration Script (`migrate_profile.py`)
For beginners, uses `db.create_all()` instead of complex migrations:

```python
def migrate_database():
    app = get_app()
    with app.app_context():
        db.create_all()
        print("✅ Database migration completed successfully!")
```

## Installation and Setup

### 1. Install Dependencies
```bash
cd app/backend
pip install -r requirements.txt
```

### 2. Run Database Migration
```bash
python migrate_profile.py
```

### 3. Create Upload Directory
```bash
mkdir uploads
mkdir uploads/profile_images
```

### 4. Start Backend Server
```bash
python main.py
```

## API Usage Examples

### Get Profile
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:5000/api/profile
```

### Update Profile
```bash
curl -X PUT \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"first_name": "John", "last_name": "Doe", "bio": "Software Engineer"}' \
     http://localhost:5000/api/profile
```

### Upload Profile Image
```bash
curl -X POST \
     -H "Authorization: Bearer <token>" \
     -F "image=@profile.jpg" \
     http://localhost:5000/api/profile/image
```

### Get Public Profile
```bash
curl http://localhost:5000/api/profile/1
```

## Security Considerations

### File Upload Security
- File type validation prevents malicious uploads
- File size limits prevent DoS attacks
- Secure file naming prevents path traversal
- Image processing removes potential embedded threats

### Data Validation
- Input sanitization prevents XSS attacks
- Length limits prevent database overflow
- Type validation ensures data integrity
- URL validation prevents malicious links

### Access Control
- JWT authentication for all profile operations
- Privacy settings control public profile access
- User can only modify their own profile

## Performance Optimizations

### Image Processing
- Automatic resizing to 800x800 maximum
- JPEG compression with 85% quality
- Format conversion for consistency
- Thumbnail generation for faster loading

### Database Optimization
- Proper indexing on user_id fields
- JSON fields for flexible data storage
- Efficient queries with proper relationships

## Error Handling

### Backend Error Responses
```json
{
  "error": "Validation errors",
  "details": [
    "First name must be 50 characters or less",
    "Invalid website URL format"
  ]
}
```

### Frontend Error Handling
- Try-catch blocks for all API calls
- User-friendly error messages
- Validation feedback
- Loading states

## Testing

### Backend Testing
- Unit tests for model validation
- API endpoint testing
- File upload testing
- Error handling testing

### Frontend Testing
- API integration testing
- Form validation testing
- Image upload testing
- Error handling testing

## Future Enhancements

### Planned Features
- Profile image cropping interface
- Bulk profile import/export
- Profile templates
- Advanced privacy controls
- Profile analytics

### Scalability Considerations
- CDN integration for image serving
- Database query optimization
- Caching strategies
- Microservice architecture

## Troubleshooting

### Common Issues

1. **File Upload Fails**
   - Check file size (max 5MB)
   - Verify file type (PNG, JPG, JPEG, GIF, WebP)
   - Ensure upload directory exists and is writable

2. **Database Migration Fails**
   - Check database connection
   - Verify MySQL server is running
   - Check database permissions

3. **Profile Update Validation Errors**
   - Review validation rules
   - Check field length limits
   - Verify data types

4. **Image Processing Errors**
   - Install Pillow library: `pip install Pillow`
   - Check available disk space
   - Verify image file integrity

### Debug Mode
Enable debug mode in Flask for detailed error messages:

```python
app.run(debug=True)
```

## Conclusion

The Profile Data Management system provides a robust, secure, and user-friendly solution for managing user profiles in the Prok Professional Networking platform. The implementation follows best practices for security, performance, and maintainability while being accessible to beginners through simple database migrations and comprehensive documentation. 