from app import app, db
import sys

try:
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        # Create all tables with new schema
        db.create_all()
        print("Database created successfully with new schema!")
except Exception as e:
    print(f"Error creating database: {e}")
    sys.exit(1)
