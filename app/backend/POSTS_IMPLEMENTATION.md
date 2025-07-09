# Posts Implementation Documentation

## Overview

This document describes the complete implementation of the post creation and management system for the Prok Professional Networking platform.

## Backend Implementation

### 1. Post Model (`models/post.py`)

The Post model includes the following features:

- **Core Fields**: id, user_id, content, created_at, updated_at
- **Media Support**: media_url, media_type (image/video)
- **Rich Content**: rich_content field for HTML-formatted content
- **Metadata**: tags (JSON), visibility settings (public/connections/private)
- **Engagement**: likes_count, comments_count
- **Soft Delete**: is_active flag for safe deletion

### 2. API Endpoints (`api/posts.py`)

#### POST `/api/posts`
- Creates a new post
- Supports multipart form data for media uploads
- Validates file types and sizes
- Handles both text and rich content

#### GET `/api/posts`
- Retrieves posts for feed or user-specific posts
- Supports pagination (limit/offset)
- Filters by user_id if provided

#### GET `/api/posts/<post_id>`
- Retrieves a specific post by ID

#### PUT `/api/posts/<post_id>`
- Updates an existing post
- Only allows post owner to update

#### DELETE `/api/posts/<post_id>`
- Soft deletes a post
- Only allows post owner to delete

#### POST `/api/posts/<post_id>/like`
- Handles post likes/unlikes
- Updates like count

### 3. Media Handling

- **File Upload**: Secure file handling with unique filenames
- **Validation**: File type and size validation
- **Storage**: Organized folder structure in uploads/posts/
- **Supported Formats**: 
  - Images: JPG, PNG, GIF, WebP
  - Videos: MP4, AVI, MOV, WMV
- **Max Size**: 10MB per file

### 4. Database Schema

```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    media_url VARCHAR(500),
    media_type VARCHAR(20),
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    rich_content TEXT,
    tags TEXT,
    visibility VARCHAR(20) DEFAULT 'public',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Frontend Implementation

### 1. PostCreate Component (`components/posts/PostCreate.tsx`)

#### Features:
- **Rich Text Editor**: Auto-resizing textarea with character count
- **Media Upload**: Drag-and-drop file upload with preview
- **Preview Mode**: Live preview of how the post will look
- **Form Validation**: Client-side validation with error messages
- **Loading States**: Visual feedback during submission
- **Visibility Settings**: Public, connections, or private posts
- **Tags Support**: Comma-separated tags with validation

#### Form Fields:
- Content (required, max 5000 chars)
- Rich Content (HTML formatting)
- Media (images/videos, max 10MB)
- Tags (comma-separated, max 200 chars)
- Visibility (radio buttons)

### 2. PostList Component (`components/posts/PostList.tsx`)

#### Features:
- **Infinite Scroll**: Load more posts with pagination
- **Media Display**: Images and videos with proper formatting
- **User Information**: Profile pictures and names
- **Engagement**: Like buttons with real-time updates
- **Time Formatting**: Relative time display (e.g., "2h ago")
- **Error Handling**: Graceful error states with retry options

### 3. API Integration (`components/posts/api.ts`)

#### Methods:
- `createPost(formData)`: Creates new post with media
- `getPosts(params)`: Fetches posts with pagination
- `likePost(postId)`: Handles post likes

## Configuration

### Backend Config (`config.py`)
```python
# File upload configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'avi', 'mov', 'wmv'}
UPLOAD_URL_PREFIX = '/uploads/'
```

## Testing

### Backend Tests
Run the test script to verify functionality:
```bash
cd app/backend
python test_posts.py
```

### Test Coverage:
- Post creation and retrieval
- Media upload handling
- Like functionality
- User-specific post filtering
- Feed generation

## Security Features

1. **Authentication**: All endpoints require JWT authentication
2. **Authorization**: Users can only edit/delete their own posts
3. **File Validation**: Strict file type and size validation
4. **SQL Injection Protection**: Parameterized queries
5. **XSS Protection**: Input sanitization for rich content

## Performance Considerations

1. **Pagination**: Efficient post loading with limit/offset
2. **Database Indexing**: Indexes on user_id and created_at
3. **Media Optimization**: Client-side image/video compression
4. **Caching**: Ready for Redis integration for post caching

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live feeds
2. **Advanced Media**: Image cropping, video thumbnails
3. **Search**: Full-text search with Elasticsearch
4. **Analytics**: Post engagement metrics
5. **Moderation**: Content filtering and reporting
6. **Comments**: Nested comment system
7. **Sharing**: Social media integration

## Usage Examples

### Creating a Post
```javascript
const formData = new FormData();
formData.append('content', 'Hello world!');
formData.append('tags', 'hello, world');
formData.append('visibility', 'public');

if (mediaFile) {
  formData.append('media', mediaFile);
}

await postsApi.createPost(formData);
```

### Fetching Posts
```javascript
const posts = await postsApi.getPosts({
  limit: 10,
  offset: 0,
  user_id: 123 // optional
});
```

### Liking a Post
```javascript
await postsApi.likePost(postId);
```

## Deployment Notes

1. **File Storage**: Ensure uploads directory is writable
2. **Database**: Run migrations to create posts table
3. **Environment**: Set proper file size limits in web server config
4. **CDN**: Consider using CDN for media file serving in production 