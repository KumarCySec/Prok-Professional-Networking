import { authenticatedRequest, apiRequest } from '../../services/api';

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
  created_at?: string;
  updated_at?: string;
}

export interface ProfileResponse {
  success: boolean;
  profile: ProfileData;
  message?: string;
}

export interface ImageUploadResponse {
  success: boolean;
  message: string;
  image_url: string;
}

export interface ErrorResponse {
  error: string;
  details?: string[];
}

/**
 * Get current user's profile
 */
export const getProfile = async (): Promise<ProfileData> => {
  try {
    const response = await authenticatedRequest('/api/profile', {
      method: 'GET',
    });
    
    if (response.success) {
      return response.profile;
    } else {
      throw new Error('Failed to fetch profile');
    }
  } catch (error) {
    console.error('Error fetching profile:', error);
    throw error;
  }
};

/**
 * Update current user's profile
 */
export const updateProfile = async (profileData: Partial<ProfileData>): Promise<ProfileData> => {
  try {
    const response = await authenticatedRequest('/api/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(profileData),
    });
    
    if (response.success) {
      return response.profile;
    } else {
      throw new Error('Failed to update profile');
    }
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
};

/**
 * Upload profile image
 */
export const uploadProfileImage = async (file: File): Promise<string> => {
  try {
    const formData = new FormData();
    formData.append('image', file);
    
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No authentication token found');
    }
    
    const response = await fetch('http://localhost:5000/api/profile/image', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        // Don't set Content-Type header for FormData, let browser set it
      },
      body: formData,
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    if (data.success) {
      return data.image_url;
    } else {
      throw new Error('Failed to upload image');
    }
  } catch (error) {
    console.error('Error uploading profile image:', error);
    throw error;
  }
};

/**
 * Delete profile image
 */
export const deleteProfileImage = async (): Promise<void> => {
  try {
    const response = await authenticatedRequest('/api/profile/image', {
      method: 'DELETE',
    });
    
    if (!response.success) {
      throw new Error('Failed to delete profile image');
    }
  } catch (error) {
    console.error('Error deleting profile image:', error);
    throw error;
  }
};

/**
 * Get public profile by user ID
 */
export const getPublicProfile = async (userId: number): Promise<ProfileData> => {
  try {
    const response = await apiRequest(`/api/profile/${userId}`, {
      method: 'GET',
    });
    
    if (response.success) {
      return response.profile;
    } else {
      throw new Error('Failed to fetch public profile');
    }
  } catch (error) {
    console.error('Error fetching public profile:', error);
    throw error;
  }
};

/**
 * Validate profile data before submission
 */
export const validateProfileData = (data: Partial<ProfileData>): string[] => {
  const errors: string[] = [];
  
  // Validate text fields
  if (data.first_name && data.first_name.length > 50) {
    errors.push('First name must be 50 characters or less');
  }
  
  if (data.last_name && data.last_name.length > 50) {
    errors.push('Last name must be 50 characters or less');
  }
  
  if (data.bio && data.bio.length > 1000) {
    errors.push('Bio must be 1000 characters or less');
  }
  
  if (data.location && data.location.length > 100) {
    errors.push('Location must be 100 characters or less');
  }
  
  if (data.company && data.company.length > 100) {
    errors.push('Company must be 100 characters or less');
  }
  
  if (data.job_title && data.job_title.length > 100) {
    errors.push('Job title must be 100 characters or less');
  }
  
  // Validate website URL
  if (data.website) {
    const urlPattern = /^https?:\/\/.+/;
    if (!urlPattern.test(data.website)) {
      errors.push('Website must be a valid URL starting with http:// or https://');
    }
  }
  
  // Validate phone number
  if (data.phone) {
    const phonePattern = /^[\d\s\-\+\(\)]+$/;
    if (!phonePattern.test(data.phone) || data.phone.replace(/\D/g, '').length < 7) {
      errors.push('Phone number must be valid and contain at least 7 digits');
    }
  }
  
  // Validate experience years
  if (data.experience_years !== undefined) {
    if (data.experience_years < 0 || data.experience_years > 50) {
      errors.push('Experience years must be between 0 and 50');
    }
  }
  
  // Validate skills array
  if (data.skills && !Array.isArray(data.skills)) {
    errors.push('Skills must be an array');
  }
  
  // Validate education array
  if (data.education && !Array.isArray(data.education)) {
    errors.push('Education must be an array');
  }
  
  // Validate social links object
  if (data.social_links && typeof data.social_links !== 'object') {
    errors.push('Social links must be an object');
  }
  
  return errors;
};

/**
 * Format profile data for display
 */
export const formatProfileData = (profile: ProfileData): ProfileData => {
  return {
    ...profile,
    // Ensure arrays are properly formatted
    skills: Array.isArray(profile.skills) ? profile.skills : [],
    education: Array.isArray(profile.education) ? profile.education : [],
    social_links: typeof profile.social_links === 'object' ? profile.social_links : {},
    // Ensure boolean fields are properly typed
    is_public: Boolean(profile.is_public),
    allow_messages: Boolean(profile.allow_messages),
    show_email: Boolean(profile.show_email),
  };
};

 