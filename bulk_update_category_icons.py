"""
Bulk update icon_class for categories.
Edit the mapping below as needed.
"""
from app import app, db
from models import Category

# Map category names to FontAwesome icon classes
CATEGORY_ICONS = {
    "Software Development": "fa-code",
    "Marketing": "fa-bullhorn",
    "Design": "fa-paint-brush",
    "Finance": "fa-chart-line",
    "Sales": "fa-handshake",
    "Human Resources": "fa-users",
    "Customer Support": "fa-headset",
    "Operations": "fa-cogs",
    "Data Science": "fa-chart-bar",
    "Product Management": "fa-tasks",
    # Add more as needed
}

with app.app_context():
    for name, icon_class in CATEGORY_ICONS.items():
        cat = Category.query.filter_by(name=name).first()
        if cat:
            cat.icon_class = icon_class
            print(f"Updated {name} -> {icon_class}")
        else:
            print(f"Category not found: {name}")
    db.session.commit()
    print("Bulk icon update complete.")
