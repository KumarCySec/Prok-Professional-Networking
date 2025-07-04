import type { Profile, ProfileFormData } from '../../types/profile';

const API_BASE_URL = 'http://localhost:5000/api';

// Get user profile
export const getProfile = async (userId?: number): Promise<Profile> => {
  try {
    const token = localStorage.getItem('token');
    const url = userId ? `${API_BASE_URL}/profile/${userId}` : `${API_BASE_URL}/profile`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch profile');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching profile:', error);
    throw error;
  }
};

// Update user profile
export const updateProfile = async (profileData: ProfileFormData): Promise<Profile> => {
  try {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(profileData)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to update profile');
    }

    return await response.json();
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
};

// Upload profile image
export const uploadProfileImage = async (file: File, type: 'avatar' | 'cover'): Promise<{ url: string }> => {
  try {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('image', file);
    formData.append('type', type);

    const response = await fetch(`${API_BASE_URL}/profile/upload-image`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to upload image');
    }

    return await response.json();
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
};

// Get user activity
export const getUserActivity = async (userId: number, page: number = 1, limit: number = 10): Promise<{
  activities: any[];
  total: number;
  hasMore: boolean;
}> => {
  try {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/profile/${userId}/activity?page=${page}&limit=${limit}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch user activity');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching user activity:', error);
    throw error;
  }
};

// Get user connections
export const getUserConnections = async (userId: number): Promise<{
  total: number;
  mutual: number;
  connections: any[];
}> => {
  try {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/profile/${userId}/connections`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Failed to fetch user connections');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching user connections:', error);
    throw error;
  }
};

// Connect with user
export const connectWithUser = async (userId: number): Promise<void> => {
  try {
    const token = localStorage.getItem('token');
    
    const response = await fetch(`${API_BASE_URL}/profile/${userId}/connect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to connect with user');
    }
  } catch (error) {
    console.error('Error connecting with user:', error);
    throw error;
  }
}; 