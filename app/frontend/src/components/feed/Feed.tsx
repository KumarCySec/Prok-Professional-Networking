import React from 'react';
import { useAuth } from '../../context/AuthContext';

const Feed: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Welcome to your Feed!</h1>
          <button
            onClick={logout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>
        
        {user && (
          <div className="bg-blue-50 p-4 rounded-lg mb-6">
            <h2 className="text-lg font-semibold mb-2">Welcome back, {user.username}!</h2>
            <p className="text-gray-600">Email: {user.email}</p>
            <p className="text-gray-600">Member since: {new Date(user.created_at || '').toLocaleDateString()}</p>
          </div>
        )}
        
        <div className="text-center text-gray-500">
          <p>Your feed content will appear here.</p>
          <p className="mt-2">
            <a href="/auth-test" className="text-blue-500 hover:underline">
              Test Authentication API
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Feed;
