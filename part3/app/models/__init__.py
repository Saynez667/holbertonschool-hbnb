from app import db
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity
from .base_model import BaseModel

def init_app(app):
    """Initialize the database with the application context."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
