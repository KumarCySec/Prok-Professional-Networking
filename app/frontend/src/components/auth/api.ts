const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

// Helper function to get auth token from localStorage
const getAuthToken = (): string | null => {
  return localStorage.getItem('token');
};

// Helper function to handle API responses
const handleResponse = async (response: Response) => {
  const data = await response.json();
  
  if (!response.ok) {
    // Throw error with message from backend
    throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
  }
  
  return data;
};

export const authApi = {
  // Login with username/email and password
  login: async (credentials: { username_or_email: string; password: string }) => {
    try {
      console.log('Attempting login with:', credentials.username_or_email);
      
      const response = await fetch(`${API_URL}/api/login`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(credentials),
      });
      
      const data = await handleResponse(response);
      
      console.log('Login successful:', data.message);
      
      return {
        success: true,
        token: data.access_token,
        user: data.user,
        message: data.message
      };
    } catch (error: any) {
      console.error('Login error:', error);
      return {
        success: false,
        message: error.message || 'Login failed'
      };
    }
  },

  // Signup with username, email, and password
  signup: async (userData: { username: string; email: string; password: string }) => {
    try {
      console.log('Attempting signup for:', userData.username);
      
      const response = await fetch(`${API_URL}/api/signup`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(userData),
      });
      
      const data = await handleResponse(response);
      
      console.log('Signup successful:', data.message);
      
      return {
        success: true,
        token: data.access_token,
        user: data.user,
        message: data.message
      };
    } catch (error: any) {
      console.error('Signup error:', error);
      return {
        success: false,
        message: error.message || 'Signup failed'
      };
    }
  },

  // Get current user info (protected endpoint)
  getCurrentUser: async () => {
    const token = getAuthToken();
    
    if (!token) {
      throw new Error('No authentication token found');
    }
    
    try {
      const response = await fetch(`${API_URL}/api/me`, {
        method: 'GET',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      });
      
      const data = await handleResponse(response);
      
      return {
        success: true,
        user: data.user
      };
    } catch (error: any) {
      return {
        success: false,
        message: error.message || 'Failed to get user info'
      };
    }
  },

  // Logout (client-side token removal)
  logout: async () => {
    const token = getAuthToken();
    
    if (token) {
      try {
        await fetch(`${API_URL}/api/logout`, {
          method: 'POST',
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
        });
      } catch (error) {
        // Even if logout fails, we still clear local storage
        console.warn('Logout request failed, but clearing local storage');
      }
    }
    
    // Always clear local storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    return { success: true };
  }
};
