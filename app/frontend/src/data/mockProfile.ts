import type { Profile } from '../types';

export const mockProfile: Profile = {
  id: 1,
  userId: 1,
  firstName: 'John',
  lastName: 'Doe',
  title: 'Senior Software Engineer',
  bio: 'Software Engineer with 5+ years of experience in full-stack development. Passionate about creating scalable web applications and mentoring junior developers.',
  location: 'San Francisco, CA',
  skills: ['JavaScript', 'TypeScript', 'React', 'Node.js', 'Python', 'PostgreSQL', 'AWS'],
  experience: [
    {
      id: 1,
      title: 'Senior Software Engineer',
      company: 'TechCorp Inc.',
      location: 'San Francisco, CA',
      startDate: '2022-01-01',
      endDate: '2024-12-31',
      description: 'Led development of microservices architecture and mentored junior developers.',
      current: true
    },
    {
      id: 2,
      title: 'Full Stack Developer',
      company: 'StartupXYZ',
      location: 'Remote',
      startDate: '2020-03-01',
      endDate: '2021-12-31',
      description: 'Built and maintained customer-facing web applications using React and Node.js.',
      current: false
    }
  ],
  education: [
    {
      id: 1,
      school: 'University of California, Berkeley',
      degree: 'Bachelor of Science',
      field: 'Computer Science',
      institution: 'University of California, Berkeley',
      gpa: '3.9',
      startDate: '2016-09-01',
      endDate: '2020-05-31',
      current: false
    }
  ],
  avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
  coverImage: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80',
  socialLinks: {
    linkedin: 'https://linkedin.com/in/johndoe',
    twitter: 'https://twitter.com/johndoe',
    github: 'https://github.com/johndoe',
    website: 'https://johndoe.dev'
  },
  contactInfo: {
    email: 'john.doe@example.com',
    phone: '+1-555-123-4567',
    address: '123 Market St, San Francisco, CA'
  },
  activity: [
    {
      id: 1,
      type: 'post',
      title: 'Published a new blog post',
      description: 'Check out my latest article on scalable React apps!',
      timestamp: '2024-07-03T10:00:00Z',
      likes: 12,
      comments: 3
    },
    {
      id: 2,
      type: 'connection',
      title: 'Connected with Jane Smith',
      description: 'Excited to connect with Jane, a fellow engineer!',
      timestamp: '2024-07-02T15:30:00Z'
    },
    {
      id: 3,
      type: 'skill',
      title: 'Added new skill: AWS',
      description: 'Started learning AWS cloud services.',
      timestamp: '2024-07-01T09:00:00Z'
    }
  ],
  connections: {
    total: 42,
    mutual: 5
  },
  createdAt: '2024-01-01T09:00:00Z',
  updatedAt: '2024-07-03T10:00:00Z'
}; 