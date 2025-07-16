#!/bin/bash

# Build script for Render deployment
set -e

echo "🚀 Starting build process..."

# Check Python version
python_version=$(python3 --version 2>&1)
echo "📋 Python version: $python_version"

# Install Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully!" 