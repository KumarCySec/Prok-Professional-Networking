import React, { useState } from 'react';
import { authApi } from './api';

const AuthTest: React.FC = () => {
  const [testResults, setTestResults] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const addResult = (message: string) => {
    setTestResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testLogin = async () => {
    setIsLoading(true);
    addResult('Testing login...');
    
    try {
      const response = await authApi.login({
        username_or_email: 'testuser',
        password: 'TestPass123!'
      });
      
      if (response.success) {
        addResult(`✅ Login successful! User: ${response.user?.username}`);
        addResult(`Token: ${response.token?.substring(0, 20)}...`);
      } else {
        addResult(`❌ Login failed: ${response.message}`);
      }
    } catch (error: any) {
      addResult(`❌ Login error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const testSignup = async () => {
    setIsLoading(true);
    addResult('Testing signup...');
    
    try {
      const response = await authApi.signup({
        username: `testuser_${Date.now()}`,
        email: `test_${Date.now()}@example.com`,
        password: 'TestPass123!'
      });
      
      if (response.success) {
        addResult(`✅ Signup successful! User: ${response.user?.username}`);
        addResult(`Token: ${response.token?.substring(0, 20)}...`);
      } else {
        addResult(`❌ Signup failed: ${response.message}`);
      }
    } catch (error: any) {
      addResult(`❌ Signup error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const testCurrentUser = async () => {
    setIsLoading(true);
    addResult('Testing get current user...');
    
    try {
      const response = await authApi.getCurrentUser();
      
      if (response.success) {
        addResult(`✅ Current user: ${response.user?.username}`);
      } else {
        addResult(`❌ Get current user failed: ${response.message}`);
      }
    } catch (error: any) {
      addResult(`❌ Get current user error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const clearResults = () => {
    setTestResults([]);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Authentication API Test</h1>
      
      <div className="space-y-4 mb-6">
        <button
          onClick={testLogin}
          disabled={isLoading}
          className="bg-blue-500 text-white px-4 py-2 rounded mr-2 disabled:opacity-50"
        >
          Test Login
        </button>
        
        <button
          onClick={testSignup}
          disabled={isLoading}
          className="bg-green-500 text-white px-4 py-2 rounded mr-2 disabled:opacity-50"
        >
          Test Signup
        </button>
        
        <button
          onClick={testCurrentUser}
          disabled={isLoading}
          className="bg-purple-500 text-white px-4 py-2 rounded mr-2 disabled:opacity-50"
        >
          Test Current User
        </button>
        
        <button
          onClick={clearResults}
          className="bg-gray-500 text-white px-4 py-2 rounded"
        >
          Clear Results
        </button>
      </div>
      
      <div className="bg-gray-100 p-4 rounded">
        <h2 className="font-semibold mb-2">Test Results:</h2>
        <div className="space-y-1">
          {testResults.map((result, index) => (
            <div key={index} className="text-sm font-mono">
              {result}
            </div>
          ))}
          {testResults.length === 0 && (
            <div className="text-gray-500">No test results yet. Click a test button above.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthTest;
