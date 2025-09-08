#!/bin/bash

# Setup script for Django FCM Notification Backend

echo "🚀 Setting up Django FCM Notification Backend..."

# Activate virtual environment
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️ Creating database migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations posts
python manage.py makemigrations notifications

echo "🔄 Applying migrations..."
python manage.py migrate

echo "👤 Creating superuser..."
python manage.py create_superuser --phone +1234567890 --password admin123

echo "✅ Setup completed!"
echo ""
echo "🔥 To start the development server:"
echo "python manage.py runserver"
echo ""
echo "📚 API Documentation will be available at:"
echo "http://127.0.0.1:8000/api/docs/"
echo ""
echo "🔐 Admin panel:"
echo "http://127.0.0.1:8000/admin/"
echo "Phone: +1234567890"
echo "Password: admin123"
echo ""
echo "⚡ To start Celery worker (for notifications):"
echo "celery -A notification_backend worker --loglevel=info --pool=eventlet --concurrency=100"
echo ""
echo "� High-performance setup with eventlet for optimal FCM delivery!"
