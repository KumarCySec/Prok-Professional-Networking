#!/bin/bash

# Quick deployment script for Render
echo "🚀 Quick Deployment Script"
echo "=========================="

echo "📝 Current changes to deploy:"
echo "✅ Added PostgreSQL URL fallback in config.py"
echo "✅ Improved database initialization in app.py"
echo "✅ Added better error handling"

echo ""
echo "📋 Next steps:"
echo "1. Commit these changes to your repository:"
echo "   git add ."
echo "   git commit -m 'Fix database configuration for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Render will automatically deploy the changes"
echo "3. Wait 2-3 minutes for deployment to complete"
echo "4. Test the endpoints:"
echo "   curl https://prok-professional-networking-dvec.onrender.com/api/db-test"
echo ""

echo "🔧 Alternative: Manual deployment in Render"
echo "1. Go to https://dashboard.render.com"
echo "2. Open your backend service: prok-professional-networking-dvec"
echo "3. Go to 'Manual Deploy' tab"
echo "4. Click 'Deploy latest commit'"
echo ""

echo "✅ After deployment, the app should use PostgreSQL instead of SQLite"
echo "✅ Login/signup should work without 503 errors" 