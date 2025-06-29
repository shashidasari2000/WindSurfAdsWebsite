#!/bin/bash

# Railway deployment script
echo "🚀 Starting Railway deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️ Initializing database..."
python init_db.py

# Run database migrations if they exist
echo "🔄 Running database migrations..."
if [ -d "migrations" ]; then
    python -c "
from flask_migrate import upgrade
from app import app
with app.app_context():
    try:
        upgrade()
        print('✅ Database migrations completed')
    except Exception as e:
        print(f'ℹ️ Migration info: {e}')
"
fi

echo "✅ Deployment preparation completed!"