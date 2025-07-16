#!/bin/bash

# Render Database Deployment Script
# This script helps automate the deployment process to Render

set -e  # Exit on any error

echo "🚀 Starting Render Database Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    print_error "This script must be run from the backend directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    print_error "pip is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ] && [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    print_status "Virtual environment found"
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        source venv/bin/activate
    fi
fi

print_success "Prerequisites check completed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning "No .env file found. Creating template..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/prok_db

# Flask Configuration
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_DEBUG=False

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:5173

# Logging
LOG_LEVEL=INFO
EOF
    print_warning "Please update the .env file with your actual values"
fi

# Test database connection if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
    print_status "Testing database connection..."
    python3 -c "
import os
from sqlalchemy import create_engine
try:
    engine = create_engine(os.environ['DATABASE_URL'])
    with engine.connect() as conn:
        result = conn.execute('SELECT 1')
        print('Database connection successful!')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"
    if [ $? -eq 0 ]; then
        print_success "Database connection test passed"
    else
        print_error "Database connection test failed"
        exit 1
    fi
else
    print_warning "DATABASE_URL not set. Skipping database connection test"
fi

# Check if migrations are set up
if [ ! -d "migrations" ]; then
    print_status "Setting up database migrations..."
    flask db init
    print_success "Migrations initialized"
fi

# Create migration if needed
print_status "Creating database migration..."
flask db migrate -m "Deployment migration"
print_success "Migration created"

# Apply migration
print_status "Applying database migration..."
flask db upgrade
print_success "Migration applied"

# Test the application
print_status "Testing application..."
python3 -c "
from app import create_app
app = create_app()
print('Application created successfully')
"

if [ $? -eq 0 ]; then
    print_success "Application test passed"
else
    print_error "Application test failed"
    exit 1
fi

# Create render.yaml if it doesn't exist
if [ ! -f "render.yaml" ]; then
    print_status "Creating render.yaml configuration..."
    cat > render.yaml << EOF
services:
  - type: web
    name: prok-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:\$PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: FLASK_DEBUG
        value: false
      - key: LOG_LEVEL
        value: INFO
EOF
    print_success "render.yaml created"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_status "Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite

# Uploads
uploads/
EOF
    print_success ".gitignore created"
fi

print_success "Deployment preparation completed!"

echo ""
echo "📋 Next Steps:"
echo "1. Go to https://render.com and create a PostgreSQL database"
echo "2. Copy the DATABASE_URL from Render"
echo "3. Update your .env file with the DATABASE_URL"
echo "4. Create a new Web Service on Render"
echo "5. Connect your GitHub repository"
echo "6. Set the environment variables in Render"
echo "7. Deploy!"
echo ""
echo "📖 For detailed instructions, see: RENDER_DATABASE_DEPLOYMENT.md"
echo ""
echo "🔧 To test locally with the new database:"
echo "   export DATABASE_URL='your-render-database-url'"
echo "   flask run"
echo "" 