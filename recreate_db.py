import os
from flask import Flask
from models import db, User, Company, Category, Job, JobType, ExperienceLevel, Skill, JobApplication, ApplicationStatus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Function to recreate the database
def recreate_database():
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            print("Dropped all tables successfully")
            
            # Create all tables
            db.create_all()
            print("Created all tables successfully")
            
            # Create default categories
            categories = [
                Category(name="Software Development"),
                Category(name="Design"),
                Category(name="Marketing"),
                Category(name="Sales"),
                Category(name="Customer Service"),
                Category(name="Finance"),
                Category(name="Human Resources"),
                Category(name="Operations")
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("Added default categories")
            
            print("Database recreated successfully!")
            return True
        except Exception as e:
            print(f"Error recreating database: {e}")
            return False

if __name__ == "__main__":
    recreate_database()
