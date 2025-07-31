@echo off
REM Deployment preparation script for Windows

echo 🚀 Preparing TODO App for Render deployment...

REM 1. Update requirements.txt
echo 📦 Updating requirements.txt...
cd backend
pip freeze > requirements.txt

REM 2. Create production environment template
echo ⚙️ Creating production environment template...
(
echo # Production Environment Variables for Render
echo FLASK_ENV=production
echo SECRET_KEY=your-super-secure-secret-key-here
echo JWT_SECRET_KEY=your-jwt-secret-key-here
echo DATABASE_URL=postgresql://user:password@host:port/database
echo MAIL_USERNAME=your-email@gmail.com
echo MAIL_PASSWORD=your-gmail-app-password
echo CORS_ORIGINS=https://your-frontend-url.onrender.com
) > .env.production

REM 3. Prepare frontend
echo 🎨 Preparing frontend...
cd ..\frontend
npm run build

echo ✅ Deployment preparation complete!
echo.
echo 📋 Next steps:
echo 1. Push code to GitHub
echo 2. Create Render account
echo 3. Deploy using render.yaml blueprint
echo 4. Configure environment variables
echo 5. Test deployment
echo.
echo 📖 See DEPLOYMENT_GUIDE.md for detailed instructions

pause
