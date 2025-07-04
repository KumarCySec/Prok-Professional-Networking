export interface Profile {
  id: number;
  userId: number;
  firstName: string;
  lastName: string;
  title: string;
  location: string;
  bio: string;
  avatar: string;
  coverImage: string;
  skills: string[];
  socialLinks: {
    linkedin?: string;
    twitter?: string;
    github?: string;
    website?: string;
  };
  contactInfo: {
    email: string;
    phone?: string;
    address?: string;
  };
  experience: Experience[];
  education: Education[];
  connections: {
    total: number;
    mutual: number;
  };
  activity: Activity[];
  createdAt: string;
  updatedAt: string;
}

export interface Experience {
  id: number;
  title: string;
  company: string;
  location: string;
  startDate: string;
  endDate?: string;
  current: boolean;
  description: string;
}

export interface Education {
  id: number;
  degree: string;
  institution: string;
  field: string;
  startDate: string;
  endDate?: string;
  current: boolean;
  gpa?: number;
}

export interface Activity {
  id: number;
  type: 'post' | 'comment' | 'connection' | 'skill';
  title: string;
  description: string;
  timestamp: string;
  likes?: number;
  comments?: number;
}

export interface ProfileFormData {
  firstName: string;
  lastName: string;
  title: string;
  location: string;
  bio: string;
  skills: string[];
  socialLinks: {
    linkedin: string;
    twitter: string;
    github: string;
    website: string;
  };
  contactInfo: {
    email: string;
    phone: string;
    address: string;
  };
} 