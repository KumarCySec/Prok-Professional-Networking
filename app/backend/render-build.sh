#!/usr/bin/env bash

# Exit on any error
set -e

echo "🚀 Starting Render deployment process..."

# Set Flask environment
export FLASK_APP=app.py
export FLASK_ENV=production

echo "📊 Running database migrations..."
# Run database migrations
flask db upgrade

echo "✅ Database migrations completed successfully"

echo "🔧 Starting Gunicorn server..."
# Start the application with Gunicorn
exec gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --preload 