import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProfile, updateProfile, uploadProfileImage, deleteProfileImage } from './api';
import type { ProfileData } from './api';
import { useAuth } from '../../context/AuthContext';

const ProfileEdit: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, refreshUser } = useAuth();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [successMessage, setSuccessMessage] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    bio: '',
    location: '',
    company: '',
    job_title: '',
    website: '',
    phone: '',
    headline: '',
    industry: '',
    current_position: '',
    company_size: '',
    linkedin_url: '',
    twitter_url: '',
    github_url: '',
    experience_years: '',
    skills: [] as string[],
    education: [] as any[],
    social_links: {} as Record<string, string>,
    is_public: true,
    allow_messages: true,
    show_email: false
  });

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      setErrors({ general: 'Please log in to edit your profile' });
      return;
    }
    fetchProfile();
  }, [isAuthenticated]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const profileData = await getProfile();
      setProfile(profileData);
      setFormData({
        first_name: profileData.first_name || '',
        last_name: profileData.last_name || '',
        bio: profileData.bio || '',
        location: profileData.location || '',
        company: profileData.company || '',
        job_title: profileData.job_title || '',
        website: profileData.website || '',
        phone: profileData.phone || '',
        headline: profileData.headline || '',
        industry: profileData.industry || '',
        current_position: profileData.current_position || '',
        company_size: profileData.company_size || '',
        linkedin_url: profileData.linkedin_url || '',
        twitter_url: profileData.twitter_url || '',
        github_url: profileData.github_url || '',
        experience_years: profileData.experience_years?.toString() || '',
        skills: Array.isArray(profileData.skills) ? profileData.skills : [],
        education: Array.isArray(profileData.education) ? profileData.education : [],
        social_links: typeof profileData.social_links === 'object' ? profileData.social_links : {},
        is_public: Boolean(profileData.is_public),
        allow_messages: Boolean(profileData.allow_messages),
        show_email: Boolean(profileData.show_email)
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
      setErrors({ general: 'Failed to load profile data. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    // Clear general error when user starts typing
    if (errors.general) {
      setErrors(prev => ({ ...prev, general: '' }));
    }
  };

  const handleSkillsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const skillsString = e.target.value;
    const skillsArray = skillsString.split(',').map(skill => skill.trim()).filter(skill => skill);
    setFormData(prev => ({ ...prev, skills: skillsArray }));
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      setErrors({ image: 'Image size must be less than 5MB' });
      return;
    }

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setErrors({ image: 'Please upload a valid image file (JPEG, PNG, GIF, WebP)' });
      return;
    }

    try {
      setUploading(true);
      setErrors(prev => ({ ...prev, image: '' }));
      const imageUrl = await uploadProfileImage(file);
      setProfile(prev => prev ? { ...prev, profile_image_url: imageUrl } : null);
      
      // Refresh user data in AuthContext to propagate the new profile image
      await refreshUser();
      
      setSuccessMessage('Profile image uploaded successfully!');
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error: any) {
      console.error('Error uploading image:', error);
      setErrors({ image: error.message || 'Failed to upload image. Please try again.' });
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteImage = async () => {
    try {
      await deleteProfileImage();
      setProfile(prev => prev ? { ...prev, profile_image_url: undefined } : null);
      
      // Refresh user data in AuthContext to propagate the profile image removal
      await refreshUser();
      
      setSuccessMessage('Profile image removed successfully!');
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error: any) {
      console.error('Error deleting image:', error);
      setErrors({ image: error.message || 'Failed to delete image. Please try again.' });
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    // Basic validations
    if (formData.first_name && formData.first_name.length > 50) {
      newErrors.first_name = 'First name must be 50 characters or less';
    }

    if (formData.last_name && formData.last_name.length > 50) {
      newErrors.last_name = 'Last name must be 50 characters or less';
    }

    if (formData.bio && formData.bio.length > 1000) {
      newErrors.bio = 'Bio must be 1000 characters or less';
    }

    if (formData.website && !/^https?:\/\/.+/.test(formData.website)) {
      newErrors.website = 'Website must be a valid URL starting with http:// or https://';
    }

    if (formData.phone && !/^[\+]?[1-9][\d]{0,15}$/.test(formData.phone.replace(/[\s\-\(\)]/g, ''))) {
      newErrors.phone = 'Please enter a valid phone number';
    }

    if (formData.experience_years) {
      const years = parseInt(formData.experience_years);
      if (isNaN(years) || years < 0 || years > 50) {
        newErrors.experience_years = 'Experience years must be between 0 and 50';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setSaving(true);
    setErrors({});
    setSuccessMessage('');
    setShowSuccess(false);

    try {
      // Clean up the data before sending - remove empty strings and undefined values
      const cleanData: any = {};
      
      Object.entries(formData).forEach(([key, value]) => {
        if (value !== '' && value !== undefined && value !== null) {
          if (key === 'experience_years' && value !== '') {
            cleanData[key] = parseInt(value as string);
          } else if (key === 'skills' && Array.isArray(value) && value.length > 0) {
            cleanData[key] = value;
          } else if (key === 'education' && Array.isArray(value) && value.length > 0) {
            cleanData[key] = value;
          } else if (key === 'social_links' && typeof value === 'object' && Object.keys(value).length > 0) {
            cleanData[key] = value;
          } else if (typeof value === 'string' && value.trim() !== '') {
            cleanData[key] = value.trim();
          } else if (typeof value === 'boolean' || typeof value === 'number') {
            cleanData[key] = value;
          }
        }
      });
      
      const updatedProfile = await updateProfile(cleanData);
      setProfile(updatedProfile);
      setSuccessMessage('Profile updated successfully!');
      setShowSuccess(true);
      
      // Navigate back to profile after 2 seconds
      setTimeout(() => {
        navigate('/profile');
      }, 2000);
    } catch (error: any) {
      console.error('Error updating profile:', error);
      
      if (error.details && Array.isArray(error.details)) {
        const errorObj: Record<string, string> = {};
        error.details.forEach((detail: string) => {
          if (detail.includes('first name')) errorObj.first_name = detail;
          else if (detail.includes('last name')) errorObj.last_name = detail;
          else if (detail.includes('website')) errorObj.website = detail;
          else if (detail.includes('phone')) errorObj.phone = detail;
          else if (detail.includes('experience')) errorObj.experience_years = detail;
          else errorObj.general = detail;
        });
        setErrors(errorObj);
      } else {
        setErrors({ general: error.message || 'Failed to update profile. Please try again.' });
      }
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg font-medium">Loading your profile...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Authentication Required</h2>
            <p className="text-gray-600 mb-6">Please log in to edit your profile.</p>
            <button
              onClick={() => navigate('/login')}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Go to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Success Toast */}
      {showSuccess && (
        <div className="fixed top-4 right-4 z-50 animate-slide-down">
          <div className="bg-green-500 text-white px-6 py-4 rounded-xl shadow-lg flex items-center space-x-3">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="font-medium">{successMessage}</span>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Edit Profile</h1>
              <p className="text-gray-600 mt-2">Update your information to keep your profile fresh and professional</p>
            </div>
            <button
              onClick={() => navigate('/profile')}
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors duration-200"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              <span>Back to Profile</span>
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Profile Image Section */}
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="flex flex-col items-center">
              <div className="relative mb-6">
                <div className="w-32 h-32 rounded-full border-4 border-white shadow-lg overflow-hidden bg-gray-100 flex items-center justify-center">
                  {profile?.profile_image_url ? (
                    <img
                      src={profile.profile_image_url}
                      alt="Profile"
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  )}
                  {uploading && (
                    <div className="absolute inset-0 bg-white/80 flex items-center justify-center">
                      <div className="animate-spin rounded-full h-8 w-8 border-2 border-blue-600 border-t-transparent"></div>
                    </div>
                  )}
                </div>
                
                {/* Upload Button */}
                <label className="absolute bottom-0 right-0 bg-blue-600 text-white rounded-full p-3 cursor-pointer shadow-lg hover:bg-blue-700 transition-colors duration-200 hover:scale-105">
                  <input
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleImageUpload}
                    disabled={uploading}
                  />
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536M9 13l3 3 8-8M21 21H3a2 2 0 01-2-2V5a2 2 0 012-2h7" />
                  </svg>
                </label>

                {/* Delete Button */}
                {profile?.profile_image_url && (
                  <button
                    type="button"
                    onClick={handleDeleteImage}
                    className="absolute top-0 right-0 bg-red-500 text-white rounded-full p-2 shadow-lg hover:bg-red-600 transition-colors duration-200 hover:scale-105"
                    disabled={uploading}
                    title="Remove image"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
              
              <div className="text-center">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Profile Photo</h3>
                <p className="text-gray-600 text-sm mb-4">Upload a professional photo to make your profile stand out</p>
                {errors.image && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
                    <p className="text-red-600 text-sm">{errors.image}</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Personal Information */}
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Personal Information</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
                <input
                  type="text"
                  name="first_name"
                  className={`w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${errors.first_name ? 'border-red-500 focus:ring-red-500' : ''}`}
                  value={formData.first_name}
                  onChange={handleInputChange}
                  maxLength={50}
                  autoComplete="given-name"
                  placeholder="Enter your first name"
                />
                {errors.first_name && <p className="text-red-600 text-sm mt-2">{errors.first_name}</p>}
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
                <input
                  type="text"
                  name="last_name"
                  className={`w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${errors.last_name ? 'border-red-500 focus:ring-red-500' : ''}`}
                  value={formData.last_name}
                  onChange={handleInputChange}
                  maxLength={50}
                  autoComplete="family-name"
                  placeholder="Enter your last name"
                />
                {errors.last_name && <p className="text-red-600 text-sm mt-2">{errors.last_name}</p>}
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                <textarea
                  name="bio"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none"
                  value={formData.bio}
                  onChange={handleInputChange}
                  maxLength={1000}
                  rows={4}
                  placeholder="Tell us about yourself, your experience, and what you're passionate about..."
                />
                <p className="text-gray-500 text-sm mt-2">{formData.bio.length}/1000 characters</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                <input
                  type="text"
                  name="location"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.location}
                  onChange={handleInputChange}
                  maxLength={100}
                  autoComplete="address-level2"
                  placeholder="City, Country"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                <input
                  type="tel"
                  name="phone"
                  className={`w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${errors.phone ? 'border-red-500 focus:ring-red-500' : ''}`}
                  value={formData.phone}
                  onChange={handleInputChange}
                  maxLength={20}
                  autoComplete="tel"
                  placeholder="+1 (555) 123-4567"
                />
                {errors.phone && <p className="text-red-600 text-sm mt-2">{errors.phone}</p>}
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Website</label>
                <input
                  type="url"
                  name="website"
                  className={`w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${errors.website ? 'border-red-500 focus:ring-red-500' : ''}`}
                  value={formData.website}
                  onChange={handleInputChange}
                  maxLength={200}
                  autoComplete="url"
                  placeholder="https://yourwebsite.com"
                />
                {errors.website && <p className="text-red-600 text-sm mt-2">{errors.website}</p>}
              </div>
            </div>
          </div>

          {/* Professional Information */}
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Professional Information</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Professional Headline</label>
                <input
                  type="text"
                  name="headline"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.headline}
                  onChange={handleInputChange}
                  maxLength={200}
                  placeholder="e.g., Senior Software Engineer"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                <input
                  type="text"
                  name="industry"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.industry}
                  onChange={handleInputChange}
                  maxLength={100}
                  placeholder="e.g., Technology, Healthcare"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Current Position</label>
                <input
                  type="text"
                  name="current_position"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.current_position}
                  onChange={handleInputChange}
                  maxLength={100}
                  placeholder="e.g., Senior Developer"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Company</label>
                <input
                  type="text"
                  name="company"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.company}
                  onChange={handleInputChange}
                  maxLength={100}
                  placeholder="e.g., Google, Microsoft"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Job Title</label>
                <input
                  type="text"
                  name="job_title"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.job_title}
                  onChange={handleInputChange}
                  maxLength={100}
                  placeholder="e.g., Software Engineer"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Company Size</label>
                <select
                  name="company_size"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white"
                  value={formData.company_size}
                  onChange={handleInputChange}
                >
                  <option value="">Select company size</option>
                  <option value="1-10">1-10 employees</option>
                  <option value="11-50">11-50 employees</option>
                  <option value="51-200">51-200 employees</option>
                  <option value="201-500">201-500 employees</option>
                  <option value="501-1000">501-1000 employees</option>
                  <option value="1000+">1000+ employees</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Years of Experience</label>
                <input
                  type="number"
                  name="experience_years"
                  className={`w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${errors.experience_years ? 'border-red-500 focus:ring-red-500' : ''}`}
                  value={formData.experience_years}
                  onChange={handleInputChange}
                  min={0}
                  max={50}
                  placeholder="5"
                />
                {errors.experience_years && <p className="text-red-600 text-sm mt-2">{errors.experience_years}</p>}
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">Skills</label>
                <input
                  type="text"
                  name="skills"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.skills.join(', ')}
                  onChange={handleSkillsChange}
                  placeholder="e.g., React, Python, Leadership, Project Management"
                />
                <p className="text-gray-500 text-sm mt-2">Separate skills with commas</p>
              </div>
            </div>
          </div>

          {/* Social Links */}
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0h10m-10 0a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Social Links</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">LinkedIn</label>
                <input
                  type="url"
                  name="linkedin_url"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.linkedin_url}
                  onChange={handleInputChange}
                  placeholder="https://linkedin.com/in/username"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Twitter</label>
                <input
                  type="url"
                  name="twitter_url"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.twitter_url}
                  onChange={handleInputChange}
                  placeholder="https://twitter.com/username"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">GitHub</label>
                <input
                  type="url"
                  name="github_url"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={formData.github_url}
                  onChange={handleInputChange}
                  placeholder="https://github.com/username"
                />
              </div>
            </div>
          </div>

          {/* Privacy Settings */}
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Privacy Settings</h3>
            </div>
            
            <div className="space-y-4">
              <label className="flex items-center p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors duration-200 cursor-pointer">
                <input
                  type="checkbox"
                  name="is_public"
                  checked={formData.is_public}
                  onChange={handleInputChange}
                  className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <div className="ml-3">
                  <span className="text-gray-900 font-medium">Public Profile</span>
                  <p className="text-gray-600 text-sm">Allow others to view your profile</p>
                </div>
              </label>
              
              <label className="flex items-center p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors duration-200 cursor-pointer">
                <input
                  type="checkbox"
                  name="allow_messages"
                  checked={formData.allow_messages}
                  onChange={handleInputChange}
                  className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <div className="ml-3">
                  <span className="text-gray-900 font-medium">Allow Messages</span>
                  <p className="text-gray-600 text-sm">Let others send you direct messages</p>
                </div>
              </label>
              
              <label className="flex items-center p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors duration-200 cursor-pointer">
                <input
                  type="checkbox"
                  name="show_email"
                  checked={formData.show_email}
                  onChange={handleInputChange}
                  className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <div className="ml-3">
                  <span className="text-gray-900 font-medium">Show Email</span>
                  <p className="text-gray-600 text-sm">Display your email address publicly</p>
                </div>
              </label>
            </div>
          </div>

          {/* Error Messages */}
          {errors.general && (
            <div className="bg-red-50 border border-red-200 rounded-xl p-6">
              <div className="flex items-center">
                <svg className="h-6 w-6 text-red-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <span className="text-red-800 font-medium">{errors.general}</span>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="bg-white rounded-2xl shadow-soft p-6">
            <div className="flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
              <button
                type="button"
                onClick={() => navigate('/profile')}
                className="w-full sm:w-auto px-8 py-3 border border-gray-300 text-gray-700 bg-white rounded-xl font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200"
                disabled={saving}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="w-full sm:w-auto px-8 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
                disabled={saving}
              >
                {saving ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                    Saving...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Save Changes
                  </>
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ProfileEdit; 