import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import PostList from '../components/posts/PostList';
import { postsApi } from '../components/posts/api';

// Mock the API
jest.mock('../components/posts/api');
const mockedPostsApi = postsApi as jest.Mocked<typeof postsApi>;

// Mock the custom hooks
jest.mock('../hooks/useInfiniteScroll', () => ({
  useInfiniteScroll: () => ({ current: null })
}));

describe('PostList Component', () => {
  const mockPosts = [
    {
      id: 1,
      user_id: 1,
      content: 'Test post 1',
      likes: 5,
      comments: [],
      tags: ['test', 'example'],
      visibility: 'public',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
      is_active: true,
      user: {
        id: 1,
        username: 'testuser',
        first_name: 'Test',
        last_name: 'User',
        profile_image_url: null
      }
    },
    {
      id: 2,
      user_id: 1,
      content: 'Test post 2',
      likes: 10,
      comments: [],
      tags: ['test'],
      visibility: 'public',
      created_at: '2024-01-02T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z',
      is_active: true,
      user: {
        id: 1,
        username: 'testuser',
        first_name: 'Test',
        last_name: 'User',
        profile_image_url: null
      }
    }
  ];

  const mockCategories = [
    { name: 'Technology', count: 10 },
    { name: 'Business', count: 5 },
    { name: 'General', count: 15 }
  ];

  const mockPopularTags = [
    { name: 'react', count: 20 },
    { name: 'javascript', count: 15 },
    { name: 'python', count: 10 }
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock API responses
    mockedPostsApi.getPosts.mockResolvedValue({
      posts: mockPosts,
      pagination: {
        page: 1,
        per_page: 20,
        total_count: 2,
        total_pages: 1,
        has_more: false
      }
    });

    mockedPostsApi.getCategories.mockResolvedValue({
      categories: mockCategories
    });

    mockedPostsApi.getPopularTags.mockResolvedValue({
      tags: mockPopularTags
    });

    mockedPostsApi.likePost.mockResolvedValue({
      message: 'Post liked successfully',
      likes_count: 6
    });
  });

  it('renders posts list with filters', async () => {
    render(<PostList />);

    // Wait for posts to load
    await waitFor(() => {
      expect(screen.getByText('Test post 1')).toBeInTheDocument();
      expect(screen.getByText('Test post 2')).toBeInTheDocument();
    });

    // Check if filters are rendered
    expect(screen.getByPlaceholderText('Search posts...')).toBeInTheDocument();
    expect(screen.getByText('Filters')).toBeInTheDocument();
  });

  it('handles search functionality', async () => {
    render(<PostList />);

    const searchInput = screen.getByPlaceholderText('Search posts...');
    
    // Type in search
    fireEvent.change(searchInput, { target: { value: 'test' } });

    // Wait for debounced search
    await waitFor(() => {
      expect(mockedPostsApi.getPosts).toHaveBeenCalledWith(
        expect.objectContaining({
          search: 'test'
        })
      );
    }, { timeout: 1000 });
  });

  it('handles filter changes', async () => {
    render(<PostList />);

    // Open advanced filters
    const filtersButton = screen.getByText('Filters');
    fireEvent.click(filtersButton);

    // Wait for filters to expand
    await waitFor(() => {
      expect(screen.getByText('Category')).toBeInTheDocument();
    });

    // Change category
    const categorySelect = screen.getByDisplayValue('All Categories');
    fireEvent.change(categorySelect, { target: { value: 'Technology' } });

    await waitFor(() => {
      expect(mockedPostsApi.getPosts).toHaveBeenCalledWith(
        expect.objectContaining({
          category: 'Technology'
        })
      );
    });
  });

  it('handles tag filtering', async () => {
    render(<PostList />);

    // Open advanced filters
    const filtersButton = screen.getByText('Filters');
    fireEvent.click(filtersButton);

    await waitFor(() => {
      expect(screen.getByText('Popular Tags')).toBeInTheDocument();
    });

    // Click on a tag
    const tagButton = screen.getByText('#react');
    fireEvent.click(tagButton);

    await waitFor(() => {
      expect(mockedPostsApi.getPosts).toHaveBeenCalledWith(
        expect.objectContaining({
          tags: ['react']
        })
      );
    });
  });

  it('handles sorting', async () => {
    render(<PostList />);

    // Change sort order
    const sortSelect = screen.getByDisplayValue('Date');
    fireEvent.change(sortSelect, { target: { value: 'likes_count' } });

    await waitFor(() => {
      expect(mockedPostsApi.getPosts).toHaveBeenCalledWith(
        expect.objectContaining({
          sort_by: 'likes_count'
        })
      );
    });
  });

  it('handles post liking', async () => {
    render(<PostList />);

    await waitFor(() => {
      expect(screen.getByText('Test post 1')).toBeInTheDocument();
    });

    // Click like button
    const likeButton = screen.getByText('5');
    fireEvent.click(likeButton);

    await waitFor(() => {
      expect(mockedPostsApi.likePost).toHaveBeenCalledWith(1);
    });
  });

  it('shows empty state when no posts', async () => {
    mockedPostsApi.getPosts.mockResolvedValue({
      posts: [],
      pagination: {
        page: 1,
        per_page: 20,
        total_count: 0,
        total_pages: 0,
        has_more: false
      }
    });

    render(<PostList />);

    await waitFor(() => {
      expect(screen.getByText('No posts found')).toBeInTheDocument();
      expect(screen.getByText('Be the first to share something!')).toBeInTheDocument();
    });
  });

  it('shows error state when API fails', async () => {
    mockedPostsApi.getPosts.mockRejectedValue(new Error('API Error'));

    render(<PostList />);

    await waitFor(() => {
      expect(screen.getByText('API Error')).toBeInTheDocument();
      expect(screen.getByText('Try Again')).toBeInTheDocument();
    });
  });

  it('handles clear filters', async () => {
    render(<PostList />);

    // Open advanced filters and add some filters
    const filtersButton = screen.getByText('Filters');
    fireEvent.click(filtersButton);

    await waitFor(() => {
      expect(screen.getByText('Category')).toBeInTheDocument();
    });

    // Change category
    const categorySelect = screen.getByDisplayValue('All Categories');
    fireEvent.change(categorySelect, { target: { value: 'Technology' } });

    // Clear filters
    const clearButton = screen.getByText('Clear all');
    fireEvent.click(clearButton);

    await waitFor(() => {
      expect(mockedPostsApi.getPosts).toHaveBeenCalledWith(
        expect.objectContaining({
          category: ''
        })
      );
    });
  });

  it('shows loading state during API calls', async () => {
    // Mock a slow API response
    mockedPostsApi.getPosts.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve({
        posts: mockPosts,
        pagination: {
          page: 1,
          per_page: 20,
          total_count: 2,
          total_pages: 1,
          has_more: false
        }
      }), 100))
    );

    render(<PostList />);

    // Should show loading state initially
    expect(screen.getByText('Loading more posts...')).toBeInTheDocument();

    // Wait for posts to load
    await waitFor(() => {
      expect(screen.getByText('Test post 1')).toBeInTheDocument();
    });
  });
}); 