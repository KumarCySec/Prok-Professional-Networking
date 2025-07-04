// Test script to verify frontend-backend integration
const API_URL = 'http://localhost:5000';

async function testBackendConnection() {
  console.log('🧪 Testing Backend Connection...');
  
  try {
    // Test signup
    const signupResponse = await fetch(`${API_URL}/api/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: 'frontend_test_user',
        email: 'frontend@test.com',
        password: 'TestPass123!'
      })
    });
    
    const signupData = await signupResponse.json();
    console.log('✅ Signup test:', signupResponse.status, signupData.message);
    
    // Test login
    const loginResponse = await fetch(`${API_URL}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username_or_email: 'frontend_test_user',
        password: 'TestPass123!'
      })
    });
    
    const loginData = await loginResponse.json();
    console.log('✅ Login test:', loginResponse.status, loginData.message);
    
    // Test protected endpoint
    const meResponse = await fetch(`${API_URL}/api/me`, {
      method: 'GET',
      headers: { 
        'Authorization': `Bearer ${loginData.access_token}`,
        'Content-Type': 'application/json'
      }
    });
    
    const meData = await meResponse.json();
    console.log('✅ Protected endpoint test:', meResponse.status);
    
    return true;
  } catch (error) {
    console.error('❌ Backend test failed:', error.message);
    return false;
  }
}

// Run test if this script is executed directly
if (typeof window === 'undefined') {
  testBackendConnection();
}
