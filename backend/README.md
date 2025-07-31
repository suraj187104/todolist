# TODO App Backend

A Flask-based REST API for a TODO application with JWT authentication, Google OAuth, and email notifications.

## Features

- 🔐 JWT-based authentication
- 🌐 Google OAuth integration
- 📧 Email notifications for new TODOs
- 📝 Full CRUD operations for TODOs
- 🗄️ PostgreSQL database
- 📊 TODO statistics and filtering
- 🚀 Ready for Render deployment

## Tech Stack

- **Framework**: Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT + Google OAuth2
- **Email**: Flask-Mail with SMTP
- **CORS**: Flask-CORS for frontend integration

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- Gmail account (for email notifications)
- Google Cloud Console project (for OAuth)

### Installation

1. **Clone and navigate to backend**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**:
   ```sql
   CREATE DATABASE todoapp;
   CREATE USER todouser WITH PASSWORD 'yourpassword';
   GRANT ALL PRIVILEGES ON DATABASE todoapp TO todouser;
   ```

5. **Configure environment**:
   ```bash
   copy .env.example .env
   # Edit .env with your database credentials, email settings, and Google OAuth
   ```

6. **Initialize database**:
   ```bash
   python setup_db.py --sample-data
   ```

7. **Run the application**:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Database
DATABASE_URL=postgresql://username:password@localhost/todoapp

# Email (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs for your frontend

### Gmail App Password

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password in Security settings
3. Use this password in `MAIL_PASSWORD`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/google` - Login with Google OAuth
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

### TODOs

- `GET /api/todos` - Get user's TODOs (with pagination/filtering)
- `POST /api/todos` - Create new TODO
- `GET /api/todos/{id}` - Get specific TODO
- `PUT /api/todos/{id}` - Update TODO
- `DELETE /api/todos/{id}` - Delete TODO
- `GET /api/todos/stats` - Get TODO statistics

### General

- `GET /` - API info
- `GET /health` - Health check

## Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

## Database Management

**Initialize database**:
```bash
python setup_db.py
```

**Add sample data**:
```bash
python setup_db.py --sample-data
```

**Reset database**:
```bash
python setup_db.py --reset
```

## Project Structure

```
backend/
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── setup_db.py        # Database setup script
├── test_api.py        # API testing script
├── .env               # Environment variables
├── models/
│   └── models.py      # Database models
├── routes/
│   ├── auth.py        # Authentication routes
│   └── todos.py       # TODO routes
└── utils/
    ├── auth.py        # JWT utilities
    ├── email_service.py # Email functions
    └── google_auth.py # Google OAuth utilities
```

## Deployment to Render

1. **Push code to GitHub**
2. **Create PostgreSQL database on Render**
3. **Create Web Service on Render**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. **Set environment variables**
5. **Deploy**

## Sample Requests

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Create TODO
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Learn Flask",
    "description": "Build a TODO app with Flask",
    "priority": "high"
  }'
```

## Common Issues

1. **Database connection error**: Check PostgreSQL is running and credentials are correct
2. **Email not sending**: Verify Gmail app password and SMTP settings
3. **Google OAuth error**: Check client ID/secret and authorized redirect URIs
4. **CORS error**: Ensure frontend URL is in CORS_ORIGINS

## License

This project is created for educational purposes as part of an internship assignment.
