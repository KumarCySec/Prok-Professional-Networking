import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from './api';
import { useAuth } from '../../context/AuthContext';

interface LoginFormData {
  username_or_email: string;
  password: string;
}

interface LoginErrors {
  username_or_email?: string;
  password?: string;
  general?: string;
}

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState<LoginFormData>({
    username_or_email: '',
    password: '',
  });
  const [errors, setErrors] = useState<LoginErrors>({});
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string>('');

  const validateForm = (): boolean => {
    const newErrors: LoginErrors = {};

    // Username/Email validation
    if (!formData.username_or_email.trim()) {
      newErrors.username_or_email = 'Username or email is required';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    
    // Clear error when user starts typing
    if (errors[name as keyof LoginErrors]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined,
      }));
    }
    
    // Clear success message when user starts typing
    if (successMessage) {
      setSuccessMessage('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setErrors({});
    setSuccessMessage('');

    try {
      console.log('Submitting login form...');
      const response = await authApi.login(formData);
      
      if (response.success) {
        // Store token and user data using AuthContext
        login(response.token!, response.user!);
        
        // Show success message
        setSuccessMessage('Login successful! Redirecting...');
        
        // Redirect to dashboard or feed after a short delay
        setTimeout(() => {
          navigate('/feed');
        }, 1000);
      } else {
        setErrors({ general: response.message || 'Login failed. Please try again.' });
      }
    } catch (error: any) {
      console.error('Login error:', error);
      setErrors({ 
        general: error.message || 'An error occurred. Please try again.' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link
              to="/signup"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              create a new account
            </Link>
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="username_or_email" className="sr-only">
                Username or Email
              </label>
              <input
                id="username_or_email"
                name="username_or_email"
                type="text"
                autoComplete="username"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.username_or_email ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm`}
                placeholder="Username or Email"
                value={formData.username_or_email}
                onChange={handleInputChange}
                disabled={isLoading}
              />
              {errors.username_or_email && (
                <p className="mt-1 text-sm text-red-600">{errors.username_or_email}</p>
              )}
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
                  errors.password ? 'border-red-300' : 'border-gray-300'
                } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm`}
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
                disabled={isLoading}
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
            </div>
          </div>

          {successMessage && (
            <div className="rounded-md bg-green-50 p-4">
              <div className="text-sm text-green-700">{successMessage}</div>
            </div>
          )}

          {errors.general && (
            <div className="rounded-md bg-red-50 p-4">
              <div className="text-sm text-red-700">{errors.general}</div>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : null}
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>

          <div className="text-center">
            <Link
              to="/signup"
              className="font-medium text-blue-600 hover:text-blue-500 text-sm"
            >
              Don't have an account? Sign up
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
