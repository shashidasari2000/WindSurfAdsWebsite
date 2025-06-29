#!/usr/bin/env python3
"""
Database initialization script for Railway deployment
"""
import os
import sys
from flask import Flask
from models import db, User, Company, Category, Job, JobType, ExperienceLevel

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configure database with proper Railway support
    def get_database_url():
        """Get the correct database URL for the environment"""
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Railway/Render provides postgres:// but SQLAlchemy needs postgresql://
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            return database_url
        
        # Fallback for local development
        return 'sqlite:///instance/jobconnect.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def init_database():
    """Initialize database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        try:
            print(f"🔗 Connecting to database: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if categories already exist
            if Category.query.count() == 0:
                # Create sample categories
                categories = [
                    Category(name="Software Development", description="Programming and software engineering roles", icon_class="fa-code", is_active=True),
                    Category(name="Marketing", description="Digital marketing and advertising positions", icon_class="fa-bullhorn", is_active=True),
                    Category(name="Design", description="UI/UX and graphic design opportunities", icon_class="fa-palette", is_active=True),
                    Category(name="Data Science", description="Analytics and data engineering roles", icon_class="fa-chart-bar", is_active=True),
                    Category(name="Product Management", description="Product strategy and management positions", icon_class="fa-tasks", is_active=True),
                    Category(name="Sales", description="Sales and business development roles", icon_class="fa-handshake", is_active=True),
                ]
                
                for category in categories:
                    db.session.add(category)
                
                db.session.commit()
                print("✅ Sample categories created successfully!")
            else:
                print("ℹ️ Categories already exist, skipping creation")
            
            # Create admin user if it doesn't exist
            admin_email = "admin@jobconnect.com"
            if not User.query.filter_by(email=admin_email).first():
                admin_user = User(
                    email=admin_email,
                    full_name="Admin User",
                    is_employer=True,
                    is_verified=True,
                    role="admin"
                )
                admin_user.set_password("admin123")  # Change this in production
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Admin user created successfully!")
                print(f"   Email: {admin_email}")
                print("   Password: admin123 (Please change this after first login)")
            else:
                print("ℹ️ Admin user already exists")
            
            print("\n🎉 Database initialization completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)