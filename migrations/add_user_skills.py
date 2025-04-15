import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import user_skills

def upgrade():
    with app.app_context():
        # Create the user_skills table
        db.create_all()
        print("Created user_skills table successfully!")

if __name__ == "__main__":
    upgrade()
