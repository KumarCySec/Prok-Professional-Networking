#!/bin/bash

# Build script for Render deployment
set -e

echo "🚀 Starting build process..."

# Force Python 3.11
echo "🐍 Setting Python version to 3.11..."
python3.11 --version || echo "Python 3.11 not available, using default"

# Check Python version
python_version=$(python3 --version 2>&1)
echo "📋 Python version: $python_version"

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create uploads directory if it doesn't exist
echo "📁 Creating uploads directory..."
mkdir -p uploads/posts uploads/profile_images

# Initialize database (optional - will be done on app startup)
echo "🗄️ Database will be initialized on app startup..."

echo "✅ Build completed successfully!" 