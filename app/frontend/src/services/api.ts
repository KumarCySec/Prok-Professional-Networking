// Use the correct backend URL - this should point to your Flask backend service
const API_URL = import.meta.env.VITE_API_URL || "https://prok-professional-networking-1-iv6a.onrender.com";

// Helper function to get auth token from localStorage
const getAuthToken = (): string | null => {
  return localStorage.getItem('token');
};

// Helper function to handle API responses
const handleResponse = async (response: Response) => {
  // Check if response is JSON
  const contentType = response.headers.get('content-type');
  if (!contentType || !contentType.includes('application/json')) {
    throw new Error(`Expected JSON response, got ${contentType}`);
  }
  
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
  }
  
  return data;
};

// Generic authenticated API request function
export const authenticatedRequest = async (
  endpoint: string, 
  options: RequestInit = {}
): Promise<any> => {
  const token = getAuthToken();
  
  if (!token) {
    throw new Error('No authentication token found');
  }
  
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    credentials: 'include',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  });
  
  return handleResponse(response);
};

// Generic API request function (for non-authenticated endpoints)
export const apiRequest = async (
  endpoint: string, 
  options: RequestInit = {}
): Promise<any> => {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    credentials: 'include',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers,
    },
  });
  
  return handleResponse(response);
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  return !!getAuthToken();
};

// Get current user from localStorage
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

// Test API connection
export const testApiConnection = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_URL}/api/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });
    
    if (response.ok) {
      const data = await response.json();
      return data.status === 'ok';
    }
    return false;
  } catch (error) {
    console.error('API connection test failed:', error);
    return false;
  }
};

// Debug API connection
export const debugApiConnection = async (): Promise<any> => {
  try {
    const response = await fetch(`${API_URL}/api/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });
    
    return {
      status: response.status,
      statusText: response.statusText,
      contentType: response.headers.get('content-type'),
      body: await response.text(),
      url: response.url
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : 'Unknown error',
      url: `${API_URL}/api/health`
    };
  }
};
