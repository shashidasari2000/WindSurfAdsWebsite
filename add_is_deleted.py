"""
One-time script to add is_deleted column to jobs table if it doesn't exist.
"""
from app import app, db
from sqlalchemy import inspect, text

with app.app_context():
    insp = inspect(db.engine)
    if 'is_deleted' not in [col['name'] for col in insp.get_columns('jobs')]:
        # Execute raw SQL using session
        db.session.execute(text('ALTER TABLE jobs ADD COLUMN is_deleted boolean DEFAULT false NOT NULL'))
        db.session.commit()
        print('Column is_deleted added to jobs table.')
    else:
        print('Column is_deleted already exists.')
