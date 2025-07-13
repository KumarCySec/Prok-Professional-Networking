import { createBrowserRouter } from 'react-router-dom';
import Login from '../components/auth/Login';
import Signup from '../components/auth/Signup';
import AuthTest from '../components/auth/AuthTest';
import ProfileView from '../components/profile/ProfileView';
import ProfileEdit from '../components/profile/ProfileEdit';
import PostCreate from '../components/posts/PostCreate';
import PostList from '../components/posts/PostList';
import Feed from '../components/feed/Feed';
import JobList from '../components/job-board/JobList';
import MessageList from '../components/messaging/MessageList';
import Navbar from '../components/navigation/Navbar';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom';

// Layout component for authenticated pages
const AuthenticatedLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg font-medium">Loading...</p>
        </div>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return (
    <div>
      <Navbar />
      {children}
    </div>
  );
};

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Navigate to="/feed" replace />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/signup',
    element: <Signup />,
  },
  {
    path: '/auth-test',
    element: <AuthTest />,
  },
  {
    path: '/feed',
    element: (
      <AuthenticatedLayout>
        <Feed />
      </AuthenticatedLayout>
    ),
  },
  {
    path: '/profile',
    element: (
      <AuthenticatedLayout>
        <ProfileView />
      </AuthenticatedLayout>
    ),
  },
  {
    path: '/profile/edit',
    element: (
      <AuthenticatedLayout>
        <ProfileEdit />
      </AuthenticatedLayout>
    ),
  },
  {
    path: '/posts/create',
    element: (
      <AuthenticatedLayout>
        <PostCreate />
      </AuthenticatedLayout>
    ),
  },
  {
    path: '/posts',
    element: (
      <AuthenticatedLayout>
        <PostList />
      </AuthenticatedLayout>
    ),
  },
  {
    path: '/jobs',
    element: (
      <AuthenticatedLayout>
        <JobList />
      </AuthenticatedLayout>
    ),
  },
  {
    path: '/messages',
    element: (
      <AuthenticatedLayout>
        <MessageList />
      </AuthenticatedLayout>
    ),
  },
]);
