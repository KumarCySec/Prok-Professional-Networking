import React, { useState, useRef, useEffect } from 'react';
import { postsApi } from './api';

interface PostFormData {
  content: string;
  rich_content: string;
  tags: string;
  visibility: 'public' | 'connections' | 'private';
  media: File | null;
}

interface PostCreateProps {
  onPostCreated?: () => void;
  onCancel?: () => void;
}

const PostCreate: React.FC<PostCreateProps> = ({ onPostCreated, onCancel }) => {
  const [formData, setFormData] = useState<PostFormData>({
    content: '',
    rich_content: '',
    tags: '',
    visibility: 'public',
    media: null
  });
  
  const [mediaPreview, setMediaPreview] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showPreview, setShowPreview] = useState(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [formData.content]);

  const handleInputChange = (field: keyof PostFormData, value: string | File) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handleMediaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        setErrors(prev => ({ ...prev, media: 'File size must be less than 10MB' }));
        return;
      }

      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'video/mp4', 'video/avi', 'video/mov', 'video/wmv'];
      if (!allowedTypes.includes(file.type)) {
        setErrors(prev => ({ ...prev, media: 'Invalid file type. Allowed: images and videos' }));
        return;
      }

      setFormData(prev => ({ ...prev, media: file }));
      setErrors(prev => ({ ...prev, media: '' }));

      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setMediaPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeMedia = () => {
    setFormData(prev => ({ ...prev, media: null }));
    setMediaPreview('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.content.trim() && !formData.rich_content.trim()) {
      newErrors.content = 'Post content is required';
    }

    if (formData.content.length > 5000) {
      newErrors.content = 'Content must be less than 5000 characters';
    }

    if (formData.tags.length > 200) {
      newErrors.tags = 'Tags must be less than 200 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    
    try {
      const formDataToSend = new FormData();
      formDataToSend.append('content', formData.content);
      formDataToSend.append('rich_content', formData.rich_content);
      formDataToSend.append('tags', formData.tags);
      formDataToSend.append('visibility', formData.visibility);
      
      if (formData.media) {
        formDataToSend.append('media', formData.media);
      }

      await postsApi.createPost(formDataToSend);
      
      // Reset form
      setFormData({
        content: '',
        rich_content: '',
        tags: '',
        visibility: 'public',
        media: null
      });
      setMediaPreview('');
      setShowPreview(false);
      
      if (onPostCreated) {
        onPostCreated();
      }
      
    } catch (error: any) {
      console.error('Error creating post:', error);
      setErrors(prev => ({ ...prev, submit: error.message || 'Failed to create post' }));
    } finally {
      setIsSubmitting(false);
    }
  };

  const togglePreview = () => {
    setShowPreview(!showPreview);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Create Post</h2>
          <div className="flex space-x-2">
            <button
              type="button"
              onClick={togglePreview}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              {showPreview ? 'Edit' : 'Preview'}
            </button>
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
            )}
          </div>
        </div>

        {showPreview ? (
          // Preview Mode
          <div className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center space-x-3 mb-3">
                <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-semibold">U</span>
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Your Name</p>
                  <p className="text-sm text-gray-500">Just now • {formData.visibility}</p>
                </div>
              </div>
              
              {formData.content && (
                <p className="text-gray-900 whitespace-pre-wrap mb-3">{formData.content}</p>
              )}
              
              {formData.rich_content && (
                <div className="text-gray-900 mb-3" dangerouslySetInnerHTML={{ __html: formData.rich_content }} />
              )}
              
              {mediaPreview && (
                <div className="mb-3">
                  {formData.media?.type.startsWith('image/') ? (
                    <img src={mediaPreview} alt="Preview" className="max-w-full h-auto rounded-lg" />
                  ) : (
                    <video controls className="max-w-full h-auto rounded-lg">
                      <source src={mediaPreview} type={formData.media?.type} />
                      Your browser does not support the video tag.
                    </video>
                  )}
                </div>
              )}
              
              {formData.tags && (
                <div className="flex flex-wrap gap-2">
                  {formData.tags.split(',').map((tag, index) => (
                    tag.trim() && (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                        #{tag.trim()}
                      </span>
                    )
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          // Edit Mode
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Content Input */}
            <div>
              <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
                What's on your mind?
              </label>
              <textarea
                ref={textareaRef}
                id="content"
                value={formData.content}
                onChange={(e) => handleInputChange('content', e.target.value)}
                placeholder="Share your thoughts, ideas, or updates..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none min-h-[120px]"
                maxLength={5000}
              />
              <div className="flex justify-between items-center mt-1">
                {errors.content && (
                  <p className="text-sm text-red-600">{errors.content}</p>
                )}
                <span className="text-sm text-gray-500">
                  {formData.content.length}/5000
                </span>
              </div>
            </div>

            {/* Rich Content Input */}
            <div>
              <label htmlFor="rich_content" className="block text-sm font-medium text-gray-700 mb-2">
                Rich Content (HTML)
              </label>
              <textarea
                id="rich_content"
                value={formData.rich_content}
                onChange={(e) => handleInputChange('rich_content', e.target.value)}
                placeholder="Add formatted content with HTML tags..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none min-h-[100px]"
              />
              <p className="text-sm text-gray-500 mt-1">
                Use HTML tags for formatting (e.g., &lt;b&gt;, &lt;i&gt;, &lt;u&gt;)
              </p>
            </div>

            {/* Media Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Add Media
              </label>
              <div className="space-y-3">
                {mediaPreview && (
                  <div className="relative">
                    {formData.media?.type.startsWith('image/') ? (
                      <img src={mediaPreview} alt="Preview" className="max-w-full h-auto rounded-lg max-h-64 object-cover" />
                    ) : (
                      <video controls className="max-w-full h-auto rounded-lg max-h-64">
                        <source src={mediaPreview} type={formData.media?.type} />
                        Your browser does not support the video tag.
                      </video>
                    )}
                    <button
                      type="button"
                      onClick={removeMedia}
                      className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600"
                    >
                      ×
                    </button>
                  </div>
                )}
                
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*,video/*"
                  onChange={handleMediaChange}
                  className="hidden"
                  id="media-upload"
                />
                <label
                  htmlFor="media-upload"
                  className="cursor-pointer inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Upload Media
                </label>
                {errors.media && (
                  <p className="text-sm text-red-600">{errors.media}</p>
                )}
                <p className="text-sm text-gray-500">
                  Supported: Images (JPG, PNG, GIF, WebP) and Videos (MP4, AVI, MOV, WMV). Max 10MB.
                </p>
              </div>
            </div>

            {/* Tags Input */}
            <div>
              <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-2">
                Tags
              </label>
              <input
                type="text"
                id="tags"
                value={formData.tags}
                onChange={(e) => handleInputChange('tags', e.target.value)}
                placeholder="Add tags separated by commas..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                maxLength={200}
              />
              <div className="flex justify-between items-center mt-1">
                {errors.tags && (
                  <p className="text-sm text-red-600">{errors.tags}</p>
                )}
                <span className="text-sm text-gray-500">
                  {formData.tags.length}/200
                </span>
              </div>
            </div>

            {/* Visibility Settings */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Visibility
              </label>
              <div className="space-y-2">
                {[
                  { value: 'public', label: 'Public', description: 'Anyone can see this post' },
                  { value: 'connections', label: 'Connections', description: 'Only your connections can see this post' },
                  { value: 'private', label: 'Private', description: 'Only you can see this post' }
                ].map((option) => (
                  <label key={option.value} className="flex items-center space-x-3">
                    <input
                      type="radio"
                      name="visibility"
                      value={option.value}
                      checked={formData.visibility === option.value}
                      onChange={(e) => handleInputChange('visibility', e.target.value as any)}
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <div>
                      <span className="text-sm font-medium text-gray-900">{option.label}</span>
                      <p className="text-sm text-gray-500">{option.description}</p>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Submit Error */}
            {errors.submit && (
              <div className="bg-red-50 border border-red-200 rounded-md p-3">
                <p className="text-sm text-red-600">{errors.submit}</p>
              </div>
            )}

            {/* Submit Button */}
            <div className="flex justify-end space-x-3">
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating...
                  </div>
                ) : (
                  'Create Post'
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default PostCreate; 