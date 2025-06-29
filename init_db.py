#!/usr/bin/env python3
"""
Database initialization script for Render deployment
"""
import os
import sys
from flask import Flask
from models import db, User, Company, Category, Job, JobType, ExperienceLevel

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configure database with proper Render support
    def get_database_url():
        """Get the correct database URL for the environment"""
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            print(f"🔗 Found DATABASE_URL: {database_url[:50]}...")
            # Render provides postgres:// but SQLAlchemy needs postgresql://
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
                print("🔄 Converted postgres:// to postgresql://")
            return database_url
        
        print("⚠️ No DATABASE_URL found - this will cause issues on Render!")
        # Fallback for local development
        return 'sqlite:///instance/jobconnect.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    print(f"🗄️ Database URI: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
    
    db.init_app(app)
    return app

def init_database():
    """Initialize database with tables and sample data"""
    print("🚀 Starting database initialization...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection first
            print("🔍 Testing database connection...")
            db.engine.execute('SELECT 1')
            print("✅ Database connection successful!")
            
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if categories already exist
            category_count = Category.query.count()
            print(f"📊 Found {category_count} existing categories")
            
            if category_count == 0:
                print("📝 Creating sample categories...")
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
                    print(f"  ➕ Added category: {category.name}")
                
                db.session.commit()
                print("✅ Sample categories created successfully!")
            else:
                print("ℹ️ Categories already exist, skipping creation")
            
            # Create admin user if it doesn't exist
            admin_email = "admin@jobconnect.com"
            existing_admin = User.query.filter_by(email=admin_email).first()
            
            if not existing_admin:
                print("👤 Creating admin user...")
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
                print(f"   📧 Email: {admin_email}")
                print("   🔑 Password: admin123 (Please change this after first login)")
            else:
                print("ℹ️ Admin user already exists")
            
            print("\n🎉 Database initialization completed successfully!")
            print("🌐 Your JobConnect app is ready to use!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Check if it's a connection error
            if "connection" in str(e).lower() or "database" in str(e).lower():
                print("\n🚨 DATABASE CONNECTION ISSUE:")
                print("   - Make sure PostgreSQL service is running on Render")
                print("   - Verify DATABASE_URL environment variable is set")
                print("   - Check if database service is properly connected to web service")
            
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 JOBCONNECT DATABASE INITIALIZATION")
    print("=" * 60)
    
    # Check for required environment variables
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not found!")
        print("   This is required for Render deployment.")
        print("   Make sure you've added a PostgreSQL database to your Render service.")
        sys.exit(1)
    
    success = init_database()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ INITIALIZATION SUCCESSFUL!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ INITIALIZATION FAILED!")
        print("=" * 60)
        sys.exit(1)