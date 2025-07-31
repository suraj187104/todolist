#!/bin/bash
# Deployment preparation script

echo "🚀 Preparing TODO App for Render deployment..."

# 1. Update requirements.txt
echo "📦 Updating requirements.txt..."
cd backend
pip freeze > requirements.txt

# 2. Create production environment template
echo "⚙️ Creating production environment template..."
cat > .env.production << EOF
# Production Environment Variables for Render
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
CORS_ORIGINS=https://your-frontend-url.onrender.com
EOF

# 3. Prepare frontend
echo "🎨 Preparing frontend..."
cd ../frontend
npm run build

echo "✅ Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Push code to GitHub"
echo "2. Create Render account"
echo "3. Deploy using render.yaml blueprint"
echo "4. Configure environment variables"
echo "5. Test deployment"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
