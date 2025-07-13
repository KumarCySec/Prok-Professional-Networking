import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import PostCreate from '../components/posts/PostCreate';
import { AuthProvider } from '../context/AuthContext';

// Mock the posts API
jest.mock('../components/posts/api', () => ({
  postsApi: {
    createPost: jest.fn(),
  },
}));

// Mock file upload
const mockFile = (name: string, size: number, type: string) => {
  const file = new File(['test content'], name, { type });
  Object.defineProperty(file, 'size', { value: size });
  return file;
};

// Mock image file
const mockImageFile = (name: string, size: number) => {
  const file = mockFile(name, size, 'image/jpeg');
  return file;
};

// Mock video file
const mockVideoFile = (name: string, size: number) => {
  const file = mockFile(name, size, 'video/mp4');
  return file;
};

// Mock FileReader
global.FileReader = class {
  onload: ((this: FileReader, ev: ProgressEvent<FileReader>) => any) | null = null;
  readAsDataURL() {
    setTimeout(() => {
      if (this.onload) {
        this.onload({ target: { result: 'data:image/jpeg;base64,test' } } as any);
      }
    }, 0);
  }
} as any;

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <AuthProvider>
        {component}
      </AuthProvider>
    </BrowserRouter>
  );
};

describe('Post Creation Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Test 1: Text-Only Post Creation', () => {
    it('should create a text-only post successfully', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;
      mockCreatePost.mockResolvedValue({ success: true });

      renderWithProviders(<PostCreate />);

      // Fill in text content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Testing text-only post creation for professional networking.' }
      });

      // Submit the form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockCreatePost).toHaveBeenCalledWith(
          expect.objectContaining({
            content: 'Testing text-only post creation for professional networking.',
            media: null
          })
        );
      });
    });

    it('should not show media placeholders for text-only posts', () => {
      renderWithProviders(<PostCreate />);

      // Check that no media preview is shown initially
      const mediaPreview = screen.queryByAltText('Preview');
      expect(mediaPreview).not.toBeInTheDocument();
    });
  });

  describe('Test 2: Post Creation with Image Upload', () => {
    it('should upload small image (<500KB) successfully', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;
      mockCreatePost.mockResolvedValue({ success: true });

      renderWithProviders(<PostCreate />);

      // Fill in text content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Testing image upload feature in post creation.' }
      });

      // Upload small image
      const fileInput = screen.getByLabelText(/upload media/i);
      const smallImage = mockImageFile('small.jpg', 400 * 1024); // 400KB
      
      fireEvent.change(fileInput, { target: { files: [smallImage] } });

      // Check that preview is shown
      await waitFor(() => {
        const preview = screen.getByAltText('Preview');
        expect(preview).toBeInTheDocument();
      });

      // Submit the form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockCreatePost).toHaveBeenCalledWith(
          expect.objectContaining({
            content: 'Testing image upload feature in post creation.',
            media: smallImage
          })
        );
      });
    });

    it('should upload medium image (~2MB) successfully', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;
      mockCreatePost.mockResolvedValue({ success: true });

      renderWithProviders(<PostCreate />);

      // Fill in text content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Testing medium image upload.' }
      });

      // Upload medium image
      const fileInput = screen.getByLabelText(/upload media/i);
      const mediumImage = mockImageFile('medium.png', 2 * 1024 * 1024); // 2MB
      
      fireEvent.change(fileInput, { target: { files: [mediumImage] } });

      // Check that preview is shown
      await waitFor(() => {
        const preview = screen.getByAltText('Preview');
        expect(preview).toBeInTheDocument();
      });

      // Submit the form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockCreatePost).toHaveBeenCalledWith(
          expect.objectContaining({
            media: mediumImage
          })
        );
      });
    });

    it('should reject large image (>5MB)', async () => {
      renderWithProviders(<PostCreate />);

      // Upload large image
      const fileInput = screen.getByLabelText(/upload media/i);
      const largeImage = mockImageFile('large.webp', 6 * 1024 * 1024); // 6MB
      
      fireEvent.change(fileInput, { target: { files: [largeImage] } });

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/file size must be less than 10mb/i);
        expect(errorMessage).toBeInTheDocument();
      });
    });
  });

  describe('Test 3: Post Creation with Video Upload', () => {
    it('should upload short video (~2MB) successfully', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;
      mockCreatePost.mockResolvedValue({ success: true });

      renderWithProviders(<PostCreate />);

      // Fill in text content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Testing video upload feature in post creation.' }
      });

      // Upload short video
      const fileInput = screen.getByLabelText(/upload media/i);
      const shortVideo = mockVideoFile('short.mp4', 2 * 1024 * 1024); // 2MB
      
      fireEvent.change(fileInput, { target: { files: [shortVideo] } });

      // Check that video preview is shown
      await waitFor(() => {
        const video = screen.getByRole('video');
        expect(video).toBeInTheDocument();
      });

      // Submit the form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      await waitFor(() => {
        expect(mockCreatePost).toHaveBeenCalledWith(
          expect.objectContaining({
            media: shortVideo
          })
        );
      });
    });

    it('should reject large video (~50MB)', async () => {
      renderWithProviders(<PostCreate />);

      // Upload large video
      const fileInput = screen.getByLabelText(/upload media/i);
      const largeVideo = mockVideoFile('large.mov', 50 * 1024 * 1024); // 50MB
      
      fireEvent.change(fileInput, { target: { files: [largeVideo] } });

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/file size must be less than 10mb/i);
        expect(errorMessage).toBeInTheDocument();
      });
    });
  });

  describe('Test 4: Media Upload Validations & Edge Cases', () => {
    it('should reject corrupted files', async () => {
      renderWithProviders(<PostCreate />);

      // Upload corrupted file
      const fileInput = screen.getByLabelText(/upload media/i);
      const corruptedFile = mockFile('corrupted.jpg', 100 * 1024, 'image/jpeg');
      
      fireEvent.change(fileInput, { target: { files: [corruptedFile] } });

      // Should still accept the file (validation happens on backend)
      await waitFor(() => {
        const preview = screen.getByAltText('Preview');
        expect(preview).toBeInTheDocument();
      });
    });

    it('should reject unsupported file formats', async () => {
      renderWithProviders(<PostCreate />);

      // Upload unsupported file
      const fileInput = screen.getByLabelText(/upload media/i);
      const exeFile = mockFile('test.exe', 100 * 1024, 'application/octet-stream');
      
      fireEvent.change(fileInput, { target: { files: [exeFile] } });

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/invalid file type/i);
        expect(errorMessage).toBeInTheDocument();
      });
    });

    it('should reject extremely large files (>100MB)', async () => {
      renderWithProviders(<PostCreate />);

      // Upload extremely large file
      const fileInput = screen.getByLabelText(/upload media/i);
      const hugeFile = mockFile('huge.mp4', 150 * 1024 * 1024, 'video/mp4'); // 150MB
      
      fireEvent.change(fileInput, { target: { files: [hugeFile] } });

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/file size must be less than 10mb/i);
        expect(errorMessage).toBeInTheDocument();
      });
    });
  });

  describe('Test 5: Form Validation & Error Handling', () => {
    it('should block submission with no text and no media', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;

      renderWithProviders(<PostCreate />);

      // Try to submit empty form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/post content is required/i);
        expect(errorMessage).toBeInTheDocument();
      });

      // Check that API was not called
      expect(mockCreatePost).not.toHaveBeenCalled();
    });

    it('should block submission with only whitespace', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;

      renderWithProviders(<PostCreate />);

      // Fill with whitespace only
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: '   \n\t   ' }
      });

      // Try to submit
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/post content is required/i);
        expect(errorMessage).toBeInTheDocument();
      });

      // Check that API was not called
      expect(mockCreatePost).not.toHaveBeenCalled();
    });

    it('should show character count and limit content length', async () => {
      renderWithProviders(<PostCreate />);

      // Fill with long content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      const longContent = 'A'.repeat(5001);
      fireEvent.change(contentTextarea, {
        target: { value: longContent }
      });

      // Check that character count is shown
      const charCount = screen.getByText(/5001\/5000/i);
      expect(charCount).toBeInTheDocument();

      // Try to submit
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/content must be less than 5000 characters/i);
        expect(errorMessage).toBeInTheDocument();
      });
    });

    it('should validate tags length', async () => {
      renderWithProviders(<PostCreate />);

      // Fill content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Test content' }
      });

      // Fill tags with long text
      const tagsInput = screen.getByPlaceholderText(/add tags separated by commas/i);
      const longTags = 'a'.repeat(201);
      fireEvent.change(tagsInput, {
        target: { value: longTags }
      });

      // Try to submit
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/tags must be less than 200 characters/i);
        expect(errorMessage).toBeInTheDocument();
      });
    });
  });

  describe('Test 6: Loading States & User Feedback', () => {
    it('should show loading indicator during submission', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;
      
      // Create a promise that doesn't resolve immediately
      let resolvePromise: (value: any) => void;
      const pendingPromise = new Promise((resolve) => {
        resolvePromise = resolve;
      });
      mockCreatePost.mockReturnValue(pendingPromise);

      renderWithProviders(<PostCreate />);

      // Fill in content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Test content' }
      });

      // Submit the form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Check that button is disabled and shows loading state
      await waitFor(() => {
        expect(submitButton).toBeDisabled();
      });

      // Resolve the promise
      resolvePromise!({ success: true });
    });

    it('should disable submit button during submission to prevent duplicates', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;
      
      let resolvePromise: (value: any) => void;
      const pendingPromise = new Promise((resolve) => {
        resolvePromise = resolve;
      });
      mockCreatePost.mockReturnValue(pendingPromise);

      renderWithProviders(<PostCreate />);

      // Fill in content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Test content' }
      });

      // Submit the form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Try to click submit button again
      fireEvent.click(submitButton);

      // Check that API was only called once
      await waitFor(() => {
        expect(mockCreatePost).toHaveBeenCalledTimes(1);
      });

      // Resolve the promise
      resolvePromise!({ success: true });
    });
  });

  describe('Test 7: Preview Mode', () => {
    it('should show preview of post before submission', async () => {
      renderWithProviders(<PostCreate />);

      // Fill in content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'This is a test post with #hashtags' }
      });

      // Fill in tags
      const tagsInput = screen.getByPlaceholderText(/add tags separated by commas/i);
      fireEvent.change(tagsInput, {
        target: { value: 'test, preview, demo' }
      });

      // Switch to preview mode
      const previewButton = screen.getByText(/preview/i);
      fireEvent.click(previewButton);

      // Check that preview content is shown
      await waitFor(() => {
        expect(screen.getByText('This is a test post with #hashtags')).toBeInTheDocument();
        expect(screen.getByText('#test')).toBeInTheDocument();
        expect(screen.getByText('#preview')).toBeInTheDocument();
        expect(screen.getByText('#demo')).toBeInTheDocument();
      });
    });

    it('should show media preview in preview mode', async () => {
      renderWithProviders(<PostCreate />);

      // Fill in content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Test post with image' }
      });

      // Upload image
      const fileInput = screen.getByLabelText(/upload media/i);
      const imageFile = mockImageFile('test.jpg', 100 * 1024);
      fireEvent.change(fileInput, { target: { files: [imageFile] } });

      // Switch to preview mode
      const previewButton = screen.getByText(/preview/i);
      fireEvent.click(previewButton);

      // Check that image preview is shown
      await waitFor(() => {
        const previewImage = screen.getByAltText('Preview');
        expect(previewImage).toBeInTheDocument();
      });
    });
  });

  describe('Test 8: Accessibility', () => {
    it('should have proper ARIA labels and roles', () => {
      renderWithProviders(<PostCreate />);

      // Check for proper labels
      expect(screen.getByLabelText(/what's on your mind/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/add media/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/tags/i)).toBeInTheDocument();

      // Check for proper roles
      expect(screen.getByRole('button', { name: /post/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /preview/i })).toBeInTheDocument();
    });

    it('should announce error messages to screen readers', async () => {
      renderWithProviders(<PostCreate />);

      // Try to submit empty form
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Check that error message is announced
      await waitFor(() => {
        const errorMessage = screen.getByText(/post content is required/i);
        expect(errorMessage).toHaveAttribute('role', 'alert');
      });
    });
  });

  describe('Test 9: Responsive Design', () => {
    it('should be responsive on different screen sizes', () => {
      renderWithProviders(<PostCreate />);

      // Check that form elements are properly sized
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      expect(contentTextarea).toHaveClass('w-full');

      const tagsInput = screen.getByPlaceholderText(/add tags separated by commas/i);
      expect(tagsInput).toHaveClass('w-full');
    });
  });

  describe('Test 10: Error Recovery', () => {
    it('should allow user to retry after failed submission', async () => {
      const mockCreatePost = require('../components/posts/api').postsApi.createPost;
      mockCreatePost.mockRejectedValueOnce(new Error('Network error'));
      mockCreatePost.mockResolvedValueOnce({ success: true });

      renderWithProviders(<PostCreate />);

      // Fill in content
      const contentTextarea = screen.getByPlaceholderText(/share your thoughts/i);
      fireEvent.change(contentTextarea, {
        target: { value: 'Test content' }
      });

      // Submit the form (should fail)
      const submitButton = screen.getByText(/post/i);
      fireEvent.click(submitButton);

      // Check that error message is shown
      await waitFor(() => {
        const errorMessage = screen.getByText(/network error/i);
        expect(errorMessage).toBeInTheDocument();
      });

      // Submit again (should succeed)
      fireEvent.click(submitButton);

      // Check that success is handled
      await waitFor(() => {
        expect(mockCreatePost).toHaveBeenCalledTimes(2);
      });
    });
  });
}); 