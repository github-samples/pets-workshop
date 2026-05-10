from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from .breed import Breed
from .dog import Dog
from .user import User

# Initialize function to be called from app.py
def init_db(app):
    db.init_app(app)
    
    # Create tables when initializing
    with app.app_context():
        db.create_all()
