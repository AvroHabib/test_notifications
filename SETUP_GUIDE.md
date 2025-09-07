# Django FCM Notification Backend - Complete Setup Guide

## 🎯 Project Overview

This is a complete Django REST Framework backend for an Android app with Firebase Cloud Messaging (FCM) push notifications. The system supports:

- **Phone number-based authentication** with JWT tokens
- **Posts and Comments** functionality
- **Real-time push notifications** via FCM
- **Comprehensive API documentation** with Swagger UI

## 📁 Project Structure

```
notification_backend/
├── accounts/                    # User authentication & device management
│   ├── models.py               # User and UserDevice models
│   ├── serializers.py          # API serializers
│   ├── views.py                # API views
│   ├── urls.py                 # URL routing
│   └── admin.py                # Django admin configuration
├── posts/                      # Posts and comments functionality
│   ├── models.py               # Post and Comment models
│   ├── serializers.py          # API serializers
│   ├── views.py                # API views
│   ├── urls.py                 # URL routing
│   └── admin.py                # Django admin configuration
├── notifications/              # FCM notifications system
│   ├── models.py               # Notification and delivery tracking
│   ├── tasks.py                # Celery background tasks
│   ├── serializers.py          # API serializers
│   ├── views.py                # API views
│   ├── urls.py                 # URL routing
│   └── admin.py                # Django admin configuration
├── notification_backend/       # Django project configuration
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Main URL routing
│   ├── celery.py               # Celery configuration
│   └── wsgi.py                 # WSGI configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── setup.sh                    # Automated setup script
├── test_api.py                 # API testing script
└── README.md                   # Documentation
```

## 🚀 Quick Start

### 1. Automated Setup
```bash
# Make setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### 2. Start the Development Server
```bash
# Activate virtual environment
source .venv/bin/activate

# Start Django server
python manage.py runserver

# The server will be available at: http://127.0.0.1:8000
```

### 3. Access API Documentation
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### 4. Default Superuser Credentials
- **Phone**: +1234567890
- **Password**: admin123

## 🔧 Manual Setup (Alternative)

### Step 1: Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database Setup
```bash
python manage.py makemigrations accounts
python manage.py makemigrations posts
python manage.py makemigrations notifications
python manage.py migrate
```

### Step 4: Create Superuser
```bash
python manage.py create_superuser --phone +1234567890 --password admin123
```

## 🔥 Firebase Configuration

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Cloud Messaging

### 2. Generate Service Account Key
1. Go to Project Settings → Service Accounts
2. Click "Generate new private key"
3. Download the JSON file
4. Save it in your project directory

### 3. Update Environment Variables
```env
# Update .env file
FIREBASE_CREDENTIALS_PATH=/path/to/your/firebase-credentials.json
```

## 📱 Android Integration

### 1. Register Device Token
After user login, register the FCM token:
```json
POST /api/auth/device/register/
{
    "fcm_token": "device_fcm_token_here",
    "device_type": "android",
    "device_id": "unique_device_identifier"
}
```

### 2. Handle Notifications
Notifications include navigation data:
```json
{
    "title": "New Post",
    "body": "John posted something new",
    "data": {
        "notification_id": "123",
        "type": "new_post",
        "action_data": "{\"type\":\"new_post\",\"post_id\":456,\"navigate_to\":\"post_detail\"}"
    }
}
```

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |
| GET/PUT | `/api/auth/profile/` | User profile |
| POST | `/api/auth/device/register/` | Register FCM device |

### Posts & Comments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/` | List all posts |
| POST | `/api/posts/create/` | Create new post |
| GET | `/api/posts/{id}/` | Get specific post |
| GET | `/api/posts/{post_id}/comments/` | List comments |
| POST | `/api/comments/create/` | Create comment |
| GET | `/api/comments/{id}/` | Get specific comment |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | List all notifications |
| GET | `/api/notifications/unread/` | List unread notifications |
| GET | `/api/notifications/count/` | Get unread count |
| POST | `/api/notifications/{id}/read/` | Mark as read |
| POST | `/api/notifications/mark-all-read/` | Mark all as read |

## ⚡ Background Tasks (Celery)

### Start Celery Worker
```bash
# Install Redis (required for Celery)
# On Ubuntu: sudo apt-get install redis-server
# On macOS: brew install redis

# Start Redis server
redis-server

# Start Celery worker
celery -A notification_backend worker --loglevel=info
```

### Notification Flow
1. **New Post**: Sends notification to all users
2. **New Comment**: Sends notification to post author

## 🧪 Testing

### API Testing Script
```bash
python test_api.py
```

### Manual Testing
1. Register a user via API
2. Login to get JWT token
3. Create a post
4. Add a comment
5. Check notifications

## 📊 Database Models

### User Model (accounts/models.py)
- Phone number-based authentication
- Profile information
- Device token management

### Post Model (posts/models.py)
- Text content
- Author relationship
- Comments count

### Notification Model (notifications/models.py)
- Notification types
- Delivery tracking
- Navigation data

## 🔒 Security Features

- JWT token authentication
- Phone number verification ready
- CORS configuration
- Input validation
- SQL injection protection

## 🌍 Production Deployment

### Environment Variables
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379/0
FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
```

### Database Migration
```bash
# For PostgreSQL
pip install psycopg2-binary
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

### Web Server
```bash
# Using Gunicorn
pip install gunicorn
gunicorn notification_backend.wsgi:application
```

## 🛠️ Development Tools

### Code Formatting
```bash
pip install black flake8 isort
black .
flake8 .
isort .
```

### Testing
```bash
python manage.py test
```

## 📞 Support

For issues and questions:
1. Check the API documentation at `/api/docs/`
2. Review the Django admin panel at `/admin/`
3. Check server logs for errors
4. Verify Firebase configuration

## 🎉 Features Implemented

✅ Phone number authentication
✅ JWT token management  
✅ Posts and comments CRUD
✅ FCM push notifications
✅ Background task processing
✅ API documentation
✅ Admin interface
✅ Device token management
✅ Notification delivery tracking
✅ Navigation data for mobile app

## 🔮 Next Steps

- Add image upload for posts
- Implement real-time messaging
- Add user following/followers
- Implement post likes/reactions
- Add push notification preferences
- Implement post categories/tags
