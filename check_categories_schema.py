from app import app, db
from sqlalchemy import text

with app.app_context():
    sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='categories'")
    result = db.session.execute(sql)
    print('Category table columns:')
    for row in result:
        print(row[0])
