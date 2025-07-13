import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { postsApi } from '../posts/api';

interface Post {
  id: number;
  user_id: number;
  content: string;
  rich_content?: string;
  media_url?: string;
  media_type?: 'image' | 'video';
  likes_count: number;
  comments_count: number;
  tags: string[];
  visibility: 'public' | 'connections' | 'private';
  category: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  user?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
    profile_image_url?: string;
  };
}

const Feed: React.FC = () => {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newPostContent, setNewPostContent] = useState('');
  const [creatingPost, setCreatingPost] = useState(false);

  // Fetch posts on component mount, but wait for auth to load
  useEffect(() => {
    if (!authLoading) {
      fetchPosts();
    }
  }, [authLoading]);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await postsApi.getPosts({
        page: 1,
        per_page: 20,
        sort_by: 'created_at',
        sort_order: 'desc'
      });
      setPosts(response.posts || []);
      setError(null);
    } catch (err: any) {
      console.error('Error fetching posts:', err);
      setError(err.message || 'Failed to load posts');
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async () => {
    if (!newPostContent.trim()) return;

    try {
      setCreatingPost(true);
      const formData = new FormData();
      formData.append('content', newPostContent);
      formData.append('visibility', 'public');
      formData.append('category', 'general');

      await postsApi.createPost(formData);
      setNewPostContent('');
      fetchPosts(); // Refresh posts
    } catch (err: any) {
      console.error('Error creating post:', err);
      setError(err.message || 'Failed to create post');
    } finally {
      setCreatingPost(false);
    }
  };

  const handleLikePost = async (postId: number) => {
    try {
      await postsApi.likePost(postId);
      fetchPosts(); // Refresh posts to get updated like count
    } catch (err: any) {
      console.error('Error liking post:', err);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours} hours ago`;
    if (diffInHours < 48) return 'Yesterday';
    return date.toLocaleDateString();
  };

  const getUserInitials = (post: Post) => {
    if (post.user?.first_name && post.user?.last_name) {
      return `${post.user.first_name[0]}${post.user.last_name[0]}`.toUpperCase();
    }
    return post.user?.username?.charAt(0).toUpperCase() || 'U';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Sidebar */}
          <div className="lg:col-span-1">
            {/* Welcome Card */}
            {user && (
              <div className="bg-white rounded-lg shadow p-6 mb-6">
                <div className="flex items-center mb-4">
                                  <div className="h-12 w-12 bg-gradient-to-r from-blue-600 to-blue-700 rounded-full flex items-center justify-center mr-4 overflow-hidden">
                  {user.profile_image_url ? (
                    <img
                      src={user.profile_image_url}
                      alt={user.username}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span className="text-white font-semibold text-lg">
                      {user.first_name?.[0] || user.username?.charAt(0).toUpperCase()}
                    </span>
                  )}
                </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Welcome back!</h3>
                    <p className="text-gray-600">@{user.username}</p>
                  </div>
                </div>
                <div className="space-y-2 text-sm text-gray-600">
                  <p>Member since: {new Date(user.created_at || '').toLocaleDateString()}</p>
                  <p>Email: {user.email}</p>
                </div>
              </div>
            )}

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button 
                  onClick={() => navigate('/posts/create')}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                >
                  <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Create Post
                </button>
                <button 
                  onClick={() => navigate('/profile')}
                  className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                >
                  <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  View Profile
                </button>
                <button 
                  onClick={() => navigate('/jobs')}
                  className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                >
                  <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                  </svg>
                  Browse Jobs
                </button>
              </div>
            </div>

            {/* Stats */}
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Stats</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Posts</span>
                  <span className="font-semibold text-gray-900">{posts.length}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Connections</span>
                  <span className="font-semibold text-gray-900">0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Profile Views</span>
                  <span className="font-semibold text-gray-900">0</span>
                </div>
              </div>
            </div>
          </div>

          {/* Main Feed */}
          <div className="lg:col-span-2">
            {/* Feed Header */}
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Your Professional Feed</h2>
              <p className="text-gray-600">Stay updated with your network and industry insights</p>
            </div>

            {/* Create Post Card */}
            <div className="bg-white rounded-lg shadow p-6 mb-6">
              <div className="flex items-start space-x-4">
                <div className="h-10 w-10 bg-gradient-to-r from-blue-600 to-blue-700 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden">
                  {user?.profile_image_url ? (
                    <img
                      src={user.profile_image_url}
                      alt={user.username}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span className="text-white font-semibold text-sm">
                      {user?.first_name?.[0] || user?.username?.charAt(0).toUpperCase()}
                    </span>
                  )}
                </div>
                <div className="flex-1">
                  <textarea
                    value={newPostContent}
                    onChange={(e) => setNewPostContent(e.target.value)}
                    className="w-full p-3 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Share your thoughts, achievements, or insights..."
                    rows={3}
                  />
                  <div className="flex justify-between items-center mt-3">
                    <div className="flex space-x-2">
                      <button className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </button>
                      <button className="p-2 text-gray-400 hover:text-blue-600 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                        </svg>
                      </button>
                    </div>
                    <button 
                      onClick={handleCreatePost}
                      disabled={creatingPost || !newPostContent.trim()}
                      className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                    >
                      {creatingPost ? 'Posting...' : 'Post'}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <p className="text-red-600">{error}</p>
              </div>
            )}

            {/* Feed Content */}
            <div className="space-y-6">
              {loading ? (
                <div className="bg-white rounded-lg shadow p-6 text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Loading posts...</p>
                </div>
              ) : posts.length > 0 ? (
                posts.map((post) => (
                  <div key={post.id} className="bg-white rounded-lg shadow">
                    <div className="p-6">
                      <div className="flex items-start space-x-4">
                        <div className="h-12 w-12 bg-gradient-to-r from-green-600 to-green-700 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden">
                          {post.user?.profile_image_url ? (
                            <img
                              src={post.user.profile_image_url}
                              alt={post.user.username}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <span className="text-white font-semibold">{getUserInitials(post)}</span>
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <h4 className="font-semibold text-gray-900">
                              {post.user?.first_name && post.user?.last_name 
                                ? `${post.user.first_name} ${post.user.last_name}`
                                : post.user?.username || 'Unknown User'
                              }
                            </h4>
                            <span className="text-gray-500">•</span>
                            <span className="text-gray-500 text-sm">{formatDate(post.created_at)}</span>
                            {post.category && (
                              <>
                                <span className="text-gray-500">•</span>
                                <span className="text-blue-600 text-sm font-medium">{post.category}</span>
                              </>
                            )}
                          </div>
                          
                          {post.content && (
                            <p className="text-gray-700 mb-4 whitespace-pre-wrap">{post.content}</p>
                          )}
                          
                          {post.rich_content && (
                            <div className="text-gray-700 mb-4" dangerouslySetInnerHTML={{ __html: post.rich_content }} />
                          )}
                          
                          {post.media_url && (
                            <div className="mb-4">
                              {post.media_type === 'image' ? (
                                <img src={post.media_url} alt="Post media" className="max-w-full h-auto rounded-lg" />
                              ) : post.media_type === 'video' ? (
                                <video controls className="max-w-full h-auto rounded-lg">
                                  <source src={post.media_url} type="video/mp4" />
                                  Your browser does not support the video tag.
                                </video>
                              ) : null}
                            </div>
                          )}
                          
                          {post.tags && post.tags.length > 0 && (
                            <div className="flex flex-wrap gap-2 mb-4">
                              {post.tags.map((tag, index) => (
                                <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                                  #{tag}
                                </span>
                              ))}
                            </div>
                          )}
                          
                          <div className="flex items-center space-x-4 text-gray-500">
                            <button 
                              onClick={() => handleLikePost(post.id)}
                              className="flex items-center space-x-1 hover:text-blue-600 transition-colors duration-200"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                              </svg>
                              <span>{post.likes_count} Like{post.likes_count !== 1 ? 's' : ''}</span>
                            </button>
                            <button className="flex items-center space-x-1 hover:text-blue-600 transition-colors duration-200">
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                              </svg>
                              <span>{post.comments_count} Comment{post.comments_count !== 1 ? 's' : ''}</span>
                            </button>
                            <button className="flex items-center space-x-1 hover:text-blue-600 transition-colors duration-200">
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                              </svg>
                              <span>Share</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="bg-white rounded-lg shadow p-6 text-center">
                  <div className="mx-auto h-16 w-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <svg className="h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">No posts yet!</h3>
                  <p className="text-gray-600 mb-6">Be the first to share something with your network.</p>
                  <button 
                    onClick={() => navigate('/posts/create')}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md font-medium transition-colors duration-200"
                  >
                    Create Your First Post
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Feed;
