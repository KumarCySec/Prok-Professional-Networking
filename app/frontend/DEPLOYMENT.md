# Frontend Deployment Configuration

## Environment Variables

Create a `.env` file in the frontend directory with the following variables:

```env
# API URL for backend (update with your production backend URL)
VITE_API_URL=https://your-backend-url.onrender.com

# Example for local development
# VITE_API_URL=http://localhost:5000
```

## Build Commands

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment Platforms

### Vercel
- Connect your GitHub repository
- Set environment variables in Vercel dashboard
- Deploy automatically on push to main branch

### Netlify
- Connect your GitHub repository
- Set environment variables in Netlify dashboard
- Build command: `npm run build`
- Publish directory: `dist`

### Render
- Connect your GitHub repository
- Set environment variables in Render dashboard
- Build command: `npm install && npm run build`
- Publish directory: `dist` 