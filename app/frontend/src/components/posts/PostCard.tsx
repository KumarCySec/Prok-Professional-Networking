import React from 'react';
import LazyImage from '../common/LazyImage';
import type { Post } from '../../types';

interface PostCardProps {
  post: Post;
  onLike: (postId: number) => void;
  likedPosts: Set<number>;
}

const PostCard: React.FC<PostCardProps> = ({ post, onLike, likedPosts }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (diffInSeconds < 60) {
      return 'Just now';
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60);
      return `${minutes}m ago`;
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600);
      return `${hours}h ago`;
    } else if (diffInSeconds < 2592000) {
      const days = Math.floor(diffInSeconds / 86400);
      return `${days}d ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const renderMedia = (post: Post) => {
    if (!post.media_url) return null;
    
    if (post.media_type === 'image') {
      return (
        <LazyImage 
          src={post.media_url} 
          alt="Post media" 
          className="w-full h-auto rounded-lg max-h-96 object-cover"
        />
      );
    } else if (post.media_type === 'video') {
      return (
        <video 
          controls 
          className="w-full h-auto rounded-lg max-h-96"
        >
          <source src={post.media_url} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      );
    }
    
    return null;
  };

  const renderTags = (tags: string[]) => {
    if (!tags || tags.length === 0) return null;
    
    return (
      <div className="flex flex-wrap gap-2 mt-2">
        {tags.map((tag, index) => (
          <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
            #{tag}
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
      {/* Post Header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center overflow-hidden">
            {post.user?.profile_image_url ? (
              <LazyImage 
                src={post.user.profile_image_url} 
                alt={post.user.username}
                className="w-10 h-10 rounded-full object-cover"
              />
            ) : (
              <span className="text-white font-semibold">
                {post.user?.first_name?.[0] || post.user?.username?.[0] || 'U'}
              </span>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-semibold text-gray-900 truncate">
              {post.user?.first_name && post.user?.last_name 
                ? `${post.user.first_name} ${post.user.last_name}`
                : post.user?.username || 'Unknown User'
              }
            </p>
            <p className="text-sm text-gray-500">
              {formatDate(post.created_at)} • {post.visibility}
            </p>
          </div>
        </div>
      </div>

      {/* Post Content */}
      <div className="p-4">
        {post.content && (
          <p className="text-gray-900 whitespace-pre-wrap mb-3 leading-relaxed">{post.content}</p>
        )}
        
        {post.rich_content && (
          <div 
            className="text-gray-900 mb-3 prose prose-sm max-w-none" 
            dangerouslySetInnerHTML={{ __html: post.rich_content }} 
          />
        )}
        
        {renderMedia(post)}
        {renderTags(post.tags || [])}
      </div>

      {/* Post Actions */}
      <div className="px-4 py-3 border-t border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <button
              onClick={() => onLike(post.id)}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-full transition-colors ${
                likedPosts.has(post.id)
                  ? 'bg-red-100 text-red-600 hover:bg-red-200'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <svg className="w-4 h-4" fill={likedPosts.has(post.id) ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              <span className="font-medium">{post.likes || 0}</span>
            </button>
            
            <button className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <span className="font-medium">{post.comments?.length || 0}</span>
            </button>
            
            <button className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
              </svg>
              <span className="font-medium">Share</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostCard; 