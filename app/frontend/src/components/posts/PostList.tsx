import React, { useState, useEffect, useCallback } from 'react';
import { postsApi } from './api';
import PostFilters from './PostFilters';
import type { PostFilters as PostFiltersType } from './PostFilters';
import PostCard from './PostCard';
import { useInfiniteScroll } from '../../hooks/useInfiniteScroll';
import type { Post } from '../../types';

interface PostListProps {
  userId?: number;
  onPostCreated?: () => void;
}

const PostList: React.FC<PostListProps> = ({ userId, onPostCreated }) => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);
  const [likedPosts, setLikedPosts] = useState<Set<number>>(new Set());
  const [categories, setCategories] = useState<string[]>([]);
  const [popularTags, setPopularTags] = useState<string[]>([]);
  const [filtersLoading, setFiltersLoading] = useState(false);

  // Default filters
  const [filters, setFilters] = useState<PostFiltersType>({
    search: '',
    category: '',
    visibility: '',
    tags: [],
    sortBy: 'created_at',
    sortOrder: 'desc'
  });

  // Fetch categories and popular tags
  const fetchFilterData = useCallback(async () => {
    try {
      setFiltersLoading(true);
      const [categoriesResponse, tagsResponse] = await Promise.all([
        postsApi.getCategories(),
        postsApi.getPopularTags()
      ]);
      
      setCategories(categoriesResponse.categories.map((cat: any) => cat.name));
      setPopularTags(tagsResponse.tags.map((tag: any) => tag.name));
    } catch (err: any) {
      console.error('Error fetching filter data:', err);
    } finally {
      setFiltersLoading(false);
    }
  }, []);

  // Fetch posts with current filters
  const fetchPosts = useCallback(async (reset = false) => {
    try {
      setLoading(true);
      const currentPage = reset ? 1 : page;
      
      const params: any = {
        page: currentPage,
        per_page: 20,
        sort_by: filters.sortBy,
        sort_order: filters.sortOrder
      };

      if (userId) {
        params.user_id = userId;
      }

      if (filters.search) {
        params.search = filters.search;
      }

      if (filters.category) {
        params.category = filters.category;
      }

      if (filters.visibility) {
        params.visibility = filters.visibility;
      }

      if (filters.tags.length > 0) {
        params.tags = filters.tags;
      }

      const response = await postsApi.getPosts(params);
      
      if (reset) {
        setPosts(response.posts);
        setPage(2);
      } else {
        setPosts(prev => [...prev, ...response.posts]);
        setPage(prev => prev + 1);
      }
      
      setHasMore(response.pagination?.has_more || false);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch posts');
    } finally {
      setLoading(false);
    }
  }, [page, filters, userId]);

  // Handle filter changes
  const handleFiltersChange = useCallback((newFilters: PostFiltersType) => {
    setFilters(newFilters);
    setPage(1);
    setHasMore(true);
  }, []);

  // Load more posts for infinite scroll
  const loadMore = useCallback(() => {
    if (!loading && hasMore) {
      fetchPosts();
    }
  }, [loading, hasMore, fetchPosts]);

  // Infinite scroll hook
  const observerRef = useInfiniteScroll({
    hasMore,
    loading,
    onLoadMore: loadMore
  });

  // Handle post like
  const handleLike = async (postId: number) => {
    try {
      await postsApi.likePost(postId);
      
      // Update posts with new like count
      setPosts(prev => prev.map(post => {
        if (post.id === postId) {
          const isLiked = likedPosts.has(postId);
          return {
            ...post,
            likes: isLiked ? post.likes - 1 : post.likes + 1
          };
        }
        return post;
      }));
      
      // Toggle liked state
      setLikedPosts(prev => {
        const newSet = new Set(prev);
        if (newSet.has(postId)) {
          newSet.delete(postId);
        } else {
          newSet.add(postId);
        }
        return newSet;
      });
    } catch (err: any) {
      console.error('Error liking post:', err);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchFilterData();
  }, [fetchFilterData]);

  // Fetch posts when filters change
  useEffect(() => {
    fetchPosts(true);
  }, [filters]);

  // Refresh posts when a new post is created
  useEffect(() => {
    if (onPostCreated) {
      fetchPosts(true);
    }
  }, [onPostCreated]);

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-600">{error}</p>
          <button 
            onClick={() => fetchPosts(true)}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      {/* Filters */}
      <PostFilters
        filters={filters}
        onFiltersChange={handleFiltersChange}
        categories={categories}
        popularTags={popularTags}
        loading={filtersLoading}
      />

      {/* Posts List */}
      <div className="space-y-6">
        {posts.length === 0 && !loading ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No posts found</h3>
            <p className="text-gray-500">
              {filters.search || filters.category || filters.visibility || filters.tags.length > 0
                ? 'Try adjusting your filters to see more posts.'
                : 'Be the first to share something!'
              }
            </p>
          </div>
        ) : (
          posts.map((post) => (
            <PostCard
              key={post.id}
              post={post}
              onLike={handleLike}
              likedPosts={likedPosts}
            />
          ))
        )}

        {/* Infinite Scroll Observer */}
        {hasMore && (
          <div ref={observerRef} className="h-10 flex items-center justify-center">
            {loading && (
              <div className="flex items-center space-x-2">
                <svg className="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="text-gray-600">Loading more posts...</span>
              </div>
            )}
          </div>
        )}

        {/* End of posts indicator */}
        {!hasMore && posts.length > 0 && (
          <div className="text-center py-8">
            <div className="inline-flex items-center space-x-2 text-gray-500">
              <div className="w-8 h-px bg-gray-300"></div>
              <span className="text-sm">You've reached the end</span>
              <div className="w-8 h-px bg-gray-300"></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PostList; 