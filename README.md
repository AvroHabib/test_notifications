# Django/DRF Backend for Android FCM Push Notifications

A Django REST Framework backend for an Android app with Firebase Cloud Messaging (FCM) push notifications support.

## Features

- **User Authentication**: Phone number-based authentication with JWT tokens
- **Posts & Comments**: Users can create posts and comment on others' posts
- **Push Notifications**: FCM integration for real-time notifications
- **API Documentation**: Auto-generated API docs with drf-spectacular
- **Celery Integration**: Background task processing for notifications

## Project Structure

```
notification_backend/
├── accounts/                 # User authentication and device management
├── posts/                   # Posts and comments functionality
├── notifications/           # FCM notifications and delivery tracking
├── notification_backend/    # Main Django project settings
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables
└── setup.sh               # Setup script
```

## Quick Setup

1. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

2. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

3. **Start Celery worker** (for notifications):
   ```bash
   celery -A notification_backend worker --loglevel=info
   ```

## Manual Setup

### 1. Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Update `.env` file with your settings:
```env
SECRET_KEY=your-secret-key
DEBUG=True
FIREBASE_CREDENTIALS_PATH=path/to/your/firebase-credentials.json
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py create_superuser --phone +1234567890 --password admin123
```

## Firebase Setup

1. **Create a Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Enable Cloud Messaging

2. **Generate Service Account Key**:
   - Go to Project Settings > Service Accounts
   - Generate new private key
   - Download the JSON file
   - Update `FIREBASE_CREDENTIALS_PATH` in `.env`

3. **Get FCM Server Key** (for Android app):
   - Go to Project Settings > Cloud Messaging
   - Copy the Server Key for your Android app

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET/PUT /api/auth/profile/` - User profile
- `POST /api/auth/device/register/` - Register FCM device token

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/create/` - Create new post
- `GET /api/posts/{id}/` - Get specific post
- `GET /api/posts/{post_id}/comments/` - List comments for a post

### Comments
- `POST /api/comments/create/` - Create new comment
- `GET /api/comments/{id}/` - Get specific comment

### Notifications
- `GET /api/notifications/` - List all notifications
- `GET /api/notifications/unread/` - List unread notifications
- `GET /api/notifications/count/` - Get unread notification count
- `POST /api/notifications/{id}/read/` - Mark notification as read
- `POST /api/notifications/mark-all-read/` - Mark all notifications as read

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **Schema**: http://127.0.0.1:8000/api/schema/

## Admin Panel

Access the Django admin at: http://127.0.0.1:8000/admin/
- Phone: +1234567890
- Password: admin123

## Notification Flow

1. **New Post Notification**:
   - User creates a post
   - Celery task sends FCM notification to all other users
   - Notification includes post ID for navigation

2. **Comment Notification**:
   - User comments on a post
   - Celery task sends FCM notification to the post author
   - Notification includes post ID and comment ID for navigation

## Android Integration

### FCM Token Registration
After user login, register the device:
```json
POST /api/auth/device/register/
{
    "fcm_token": "device_fcm_token_here",
    "device_type": "android",
    "device_id": "unique_device_identifier"
}
```

### Notification Payload
Notifications will include:
```json
{
    "title": "New Post",
    "body": "John Doe posted something new",
    "data": {
        "notification_id": "123",
        "type": "new_post",
        "action_data": "{\"type\":\"new_post\",\"post_id\":456,\"navigate_to\":\"post_detail\"}"
    }
}
```

### Navigation Handling
Parse `action_data` to determine navigation:
- `new_post`: Navigate to post detail screen
- `new_comment`: Navigate to comment detail screen

## Development

### Testing
```bash
python manage.py test
```

### Code Quality
```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .

# Check code style
flake8 .

# Sort imports
isort .
```

## Production Deployment

1. **Update settings for production**:
   - Set `DEBUG=False`
   - Configure production database (PostgreSQL)
   - Set up Redis for Celery
   - Configure static file serving

2. **Environment variables**:
   ```env
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=postgresql://user:pass@localhost/db
   REDIS_URL=redis://localhost:6379/0
   ```

3. **Static files**:
   ```bash
   python manage.py collectstatic
   ```

4. **Run with Gunicorn**:
   ```bash
   gunicorn notification_backend.wsgi:application
   ```

## Troubleshooting

### Common Issues

1. **Firebase credentials not found**:
   - Ensure `FIREBASE_CREDENTIALS_PATH` points to valid JSON file
   - Check file permissions

2. **Celery not processing tasks**:
   - Ensure Redis is running
   - Check Celery worker is started
   - Verify `CELERY_BROKER_URL` configuration

3. **FCM token invalid**:
   - Tokens are automatically deactivated when invalid
   - Ensure Android app regenerates tokens when needed

### Logs

Check logs for debugging:
```bash
# Django logs
python manage.py runserver --verbosity=2

# Celery logs
celery -A notification_backend worker --loglevel=debug
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
