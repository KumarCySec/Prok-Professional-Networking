import React from 'react';

interface ImageUploadProps {
  label: string;
  preview: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  aspectRatio?: 'square' | 'wide';
  className?: string;
}

const ImageUpload: React.FC<ImageUploadProps> = ({
  label,
  preview,
  onChange,
  error,
  aspectRatio = 'square',
  className = ''
}) => {
  const containerClasses = aspectRatio === 'square' 
    ? 'w-20 h-20 rounded-full' 
    : 'w-full h-24 rounded-lg';
  
  const containerClassesWithBg = `${containerClasses} overflow-hidden bg-gray-100 ${className}`;

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      <div className="space-y-2">
        <div className={containerClassesWithBg}>
          {preview ? (
            <img
              src={preview}
              alt="Preview"
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          )}
        </div>
        <input
          type="file"
          accept="image/*"
          onChange={onChange}
          className="hidden"
          id={`${label.toLowerCase().replace(/\s+/g, '-')}-upload`}
        />
        <label
          htmlFor={`${label.toLowerCase().replace(/\s+/g, '-')}-upload`}
          className="cursor-pointer inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          Upload {label}
        </label>
        {error && (
          <p className="mt-1 text-sm text-red-600">{error}</p>
        )}
      </div>
    </div>
  );
};

export default ImageUpload; 