import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProfile } from './api';
import type { ProfileData } from './api';
import { useAuth } from '../../context/AuthContext';

// Social Media Icons Component
const SocialIcon: React.FC<{ platform: string; url?: string }> = ({ platform, url }) => {
  if (!url) return null;
  
  const icons = {
    linkedin: 'M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z',
    twitter: 'M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z',
    github: 'M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.237 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z',
    website: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z'
  };

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gray-100 hover:bg-blue-100 transition-all duration-200 hover:scale-110 shadow-sm"
      title={platform}
    >
      <svg className="w-6 h-6 text-gray-600 hover:text-blue-600" fill="currentColor" viewBox="0 0 24 24">
        <path d={icons[platform as keyof typeof icons]} />
      </svg>
    </a>
  );
};

// Info Card Component
const InfoCard: React.FC<{
  title: string;
  icon: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}> = ({ title, icon, children, className = '' }) => {
  return (
    <div className={`bg-white rounded-2xl shadow-soft p-6 ${className}`}>
      <div className="flex items-center mb-4">
        <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
          {icon}
        </div>
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      </div>
      {children}
    </div>
  );
};

// Skill Badge Component
const SkillBadge: React.FC<{ skill: string }> = ({ skill }) => {
  return (
    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 mr-2 mb-2">
      {skill}
    </span>
  );
};

const ProfileView: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false);
      setError('Please log in to view your profile');
      return;
    }
    
    fetchProfile();
  }, [isAuthenticated]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const profileData = await getProfile();
      setProfile(profileData);
    } catch (err: any) {
      console.error('Error fetching profile:', err);
      if (err.message?.includes('No authentication token found') || err.message?.includes('401')) {
        setError('Please log in to view your profile');
      } else {
        setError(err.message || 'Failed to load profile');
      }
    } finally {
      setLoading(false);
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

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Error loading profile</h2>
            <p className="text-gray-600 mb-6">{error}</p>
            <div className="space-x-4">
              {error.includes('log in') ? (
                <button
                  onClick={() => navigate('/login')}
                  className="w-full bg-blue-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Go to Login
                </button>
              ) : (
                <button
                  onClick={fetchProfile}
                  className="w-full bg-blue-600 text-white py-3 px-6 rounded-xl font-medium hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Try Again
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Profile not found</h2>
            <p className="text-gray-600">The profile you're looking for doesn't exist.</p>
          </div>
        </div>
      </div>
    );
  }

  const fullName = `${profile.first_name || ''} ${profile.last_name || ''}`.trim() || profile.username || 'User';
  const hasSkills = profile.skills && Array.isArray(profile.skills) && profile.skills.length > 0;
  const hasEducation = profile.education && Array.isArray(profile.education) && profile.education.length > 0;
  const hasSocialLinks = profile.linkedin_url || profile.twitter_url || profile.github_url || profile.website;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
              <p className="text-gray-600 mt-2">View and manage your professional profile</p>
            </div>
            <button
              onClick={() => navigate('/profile/edit')}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-sm hover:shadow-md"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Edit Profile
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Profile Info */}
          <div className="lg:col-span-1 space-y-6">
            {/* Profile Card */}
            <div className="bg-white rounded-2xl shadow-soft overflow-hidden">
              {/* Cover Image */}
              <div className="relative h-32 bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600">
                <div className="absolute inset-0 bg-black bg-opacity-10"></div>
              </div>
              
              {/* Profile Info */}
              <div className="relative px-6 pb-6">
                {/* Avatar */}
                <div className="absolute -top-16 left-6">
                  <div className="w-32 h-32 rounded-full border-4 border-white shadow-lg overflow-hidden bg-gray-100">
                    {profile.profile_image_url ? (
                      <img
                        src={profile.profile_image_url}
                        alt={fullName}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        <svg className="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </div>
                    )}
                  </div>
                </div>

                {/* Profile Details */}
                <div className="pt-20">
                  <h2 className="text-2xl font-bold text-gray-900 mb-1">{fullName}</h2>
                  {profile.headline && (
                    <p className="text-gray-600 mb-3">{profile.headline}</p>
                  )}
                  {profile.company && (
                    <p className="text-gray-500 text-sm mb-4">
                      <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      {profile.company}
                      {profile.job_title && ` • ${profile.job_title}`}
                    </p>
                  )}
                  {profile.location && (
                    <p className="text-gray-500 text-sm mb-4">
                      <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      {profile.location}
                    </p>
                  )}
                  
                  {/* Contact Info */}
                  {(profile.phone || profile.website) && (
                    <div className="space-y-2 mb-4">
                      {profile.phone && (
                        <p className="text-gray-500 text-sm">
                          <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                          </svg>
                          {profile.phone}
                        </p>
                      )}
                      {profile.website && (
                        <p className="text-gray-500 text-sm">
                          <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                          </svg>
                          <a href={profile.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700">
                            {profile.website.replace(/^https?:\/\//, '')}
                          </a>
                        </p>
                      )}
                    </div>
                  )}

                  {/* Social Links */}
                  {hasSocialLinks && (
                    <div className="flex space-x-3">
                      {profile.linkedin_url && <SocialIcon platform="linkedin" url={profile.linkedin_url} />}
                      {profile.twitter_url && <SocialIcon platform="twitter" url={profile.twitter_url} />}
                      {profile.github_url && <SocialIcon platform="github" url={profile.github_url} />}
                      {profile.website && <SocialIcon platform="website" url={profile.website} />}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Skills */}
            {hasSkills && (
              <InfoCard
                title="Skills"
                icon={
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                }
              >
                <div className="flex flex-wrap">
                  {profile.skills?.map((skill, index) => (
                    <SkillBadge key={index} skill={skill} />
                  ))}
                </div>
              </InfoCard>
            )}

            {/* Privacy Settings */}
            <InfoCard
              title="Privacy Settings"
              icon={
                <svg className="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              }
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">Public Profile</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${profile.is_public ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {profile.is_public ? 'Public' : 'Private'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">Allow Messages</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${profile.allow_messages ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {profile.allow_messages ? 'Enabled' : 'Disabled'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">Show Email</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${profile.show_email ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {profile.show_email ? 'Visible' : 'Hidden'}
                  </span>
                </div>
              </div>
            </InfoCard>
          </div>

          {/* Right Column - Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* About */}
            {profile.bio && (
              <InfoCard
                title="About"
                icon={
                  <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                }
              >
                <p className="text-gray-700 leading-relaxed">{profile.bio}</p>
              </InfoCard>
            )}

            {/* Professional Information */}
            {(profile.headline || profile.industry || profile.current_position || profile.company || profile.job_title || profile.company_size || profile.experience_years) && (
              <InfoCard
                title="Professional Information"
                icon={
                  <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6" />
                  </svg>
                }
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {profile.headline && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">Professional Headline</label>
                      <p className="text-gray-900">{profile.headline}</p>
                    </div>
                  )}
                  {profile.industry && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">Industry</label>
                      <p className="text-gray-900">{profile.industry}</p>
                    </div>
                  )}
                  {profile.current_position && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">Current Position</label>
                      <p className="text-gray-900">{profile.current_position}</p>
                    </div>
                  )}
                  {profile.company && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">Company</label>
                      <p className="text-gray-900">{profile.company}</p>
                    </div>
                  )}
                  {profile.job_title && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">Job Title</label>
                      <p className="text-gray-900">{profile.job_title}</p>
                    </div>
                  )}
                  {profile.company_size && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">Company Size</label>
                      <p className="text-gray-900">{profile.company_size} employees</p>
                    </div>
                  )}
                  {profile.experience_years && (
                    <div>
                      <label className="block text-sm font-medium text-gray-500 mb-1">Years of Experience</label>
                      <p className="text-gray-900">{profile.experience_years} years</p>
                    </div>
                  )}
                </div>
              </InfoCard>
            )}

            {/* Education */}
            {hasEducation && (
              <InfoCard
                title="Education"
                icon={
                  <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                  </svg>
                }
              >
                <div className="space-y-4">
                  {profile.education?.map((edu, index) => (
                    <div key={index} className="border-l-4 border-purple-200 pl-4">
                      <h4 className="font-medium text-gray-900">{edu.school || edu.institution}</h4>
                      <p className="text-gray-600">{edu.degree} in {edu.field}</p>
                      <p className="text-sm text-gray-500">
                        {edu.startDate} - {edu.current ? 'Present' : edu.endDate}
                      </p>
                    </div>
                  ))}
                </div>
              </InfoCard>
            )}

            {/* Profile Stats */}
            <InfoCard
              title="Profile Statistics"
              icon={
                <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              }
            >
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{profile.skills?.length || 0}</div>
                  <div className="text-sm text-gray-500">Skills</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{profile.education?.length || 0}</div>
                  <div className="text-sm text-gray-500">Education</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{profile.experience_years || 0}</div>
                  <div className="text-sm text-gray-500">Years Experience</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600">
                    {[profile.linkedin_url, profile.twitter_url, profile.github_url, profile.website].filter(Boolean).length}
                  </div>
                  <div className="text-sm text-gray-500">Social Links</div>
                </div>
              </div>
            </InfoCard>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileView; 