# 📝 TODO App - Full Stack Application

A modern, full-stack TODO application built with Flask (backend) and React (frontend), featuring JWT authentication, email notifications, and real-time task management.

## 🌟 Features

### ✅ **Authentication**
- User registration and login
- JWT-based authentication
- Google OAuth integration (ready)
- Password hashing with bcrypt

### ✅ **Task Management**
- Create, read, update, delete TODOs
- Priority levels (High, Medium, Low)
- Task completion tracking
- Real-time statistics

### ✅ **Email Notifications**
- Automatic email on TODO creation
- Gmail SMTP integration
- Customizable email templates

### ✅ **User Experience**
- Responsive design with Tailwind CSS
- Loading states and error handling
- Task filtering and sorting
- Progress tracking dashboard

## 🏗️ Architecture

```
todo-app/
├── backend/                 # Flask API
│   ├── app.py              # Main application
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── utils/              # Utilities
│   └── config.py           # Configuration
├── frontend/               # React SPA
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   └── services/       # API services
│   └── public/
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Local Development

1. **Clone & Setup**
```bash
git clone <your-repo-url>
cd todo-app
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configure your environment variables
python app.py
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

4. **Access Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 🌐 Deployment

### Render (Recommended)
1. Push code to GitHub
2. Create account on [Render](https://render.com)
3. Use the included `render.yaml` blueprint
4. Configure environment variables
5. Deploy!

**Detailed deployment guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🔧 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=your-database-url
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh token

### TODOs
- `GET /api/todos` - Get user's TODOs
- `POST /api/todos` - Create new TODO
- `PUT /api/todos/{id}` - Update TODO
- `DELETE /api/todos/{id}` - Delete TODO
- `GET /api/todos/stats` - Get TODO statistics

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Testing
```bash
cd backend
python test_api.py
```

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Flask-Mail** - Email
- **bcrypt** - Password hashing
- **PostgreSQL/SQLite** - Database

### Frontend
- **React** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Context API** - State management

### Deployment
- **Render** - Hosting platform
- **PostgreSQL** - Production database
- **Gunicorn** - WSGI server

## 📊 Project Status

- ✅ **Backend API** - Complete
- ✅ **Frontend UI** - Complete
- ✅ **Authentication** - Working
- ✅ **Database** - Configured
- ✅ **Email System** - Configured
- ✅ **Deployment Ready** - Yes
- 🔄 **Google OAuth** - Ready to configure
- 🔄 **Advanced Features** - In progress

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
- Check the [deployment guide](DEPLOYMENT_GUIDE.md)
- Review the [quick start guide](QUICK_START.md)
- Create an issue on GitHub

---

**Built with ❤️ for modern web development**
