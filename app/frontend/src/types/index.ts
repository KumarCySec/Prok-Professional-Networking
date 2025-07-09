export interface User {
  id: number;
  username: string;
  email: string;
  name: string;
  created_at: string;
}

export interface Profile {
  id: number;
  userId: number;
  firstName: string;
  lastName: string;
  title: string;
  bio: string;
  location: string;
  skills: string[];
  experience: Experience[];
  education: Education[];
  avatar: string;
  coverImage: string;
  socialLinks: SocialLinks;
  contactInfo: ContactInfo;
  activity: Activity[];
  connections: {
    total: number;
    mutual: number;
  };
  createdAt: string;
  updatedAt: string;
}

export interface Experience {
  id: number;
  title: string;
  company: string;
  location: string;
  startDate: string;
  endDate: string;
  description: string;
  current: boolean;
}

export interface Education {
  id: number;
  school: string;
  degree: string;
  field: string;
  institution: string;
  gpa?: string;
  startDate: string;
  endDate: string;
  current: boolean;
}

export interface Post {
  id: number;
  user_id: number;
  content: string;
  rich_content?: string;
  media_url?: string;
  media_type?: 'image' | 'video';
  likes: number;
  comments: Comment[];
  tags: string[];
  visibility: 'public' | 'connections' | 'private';
  created_at: string;
  updated_at: string;
  is_active: boolean;
  user?: {
    id: number;
    username: string;
    first_name?: string;
    last_name?: string;
    profile_image_url?: string;
  };
}

export interface Comment {
  id: number;
  user_id: number;
  content: string;
  created_at: string;
}

export interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements: string[];
  created_at: string;
}

export interface Message {
  id: number;
  sender_id: number;
  receiver_id: number;
  content: string;
  created_at: string;
  read: boolean;
}

export interface SocialLinks {
  linkedin?: string;
  twitter?: string;
  github?: string;
  website?: string;
}

export interface ContactInfo {
  email: string;
  phone: string;
  address?: string;
}

export interface Activity {
  id: number;
  type: string;
  title: string;
  description: string;
  timestamp: string;
  likes?: number;
  comments?: number;
} 