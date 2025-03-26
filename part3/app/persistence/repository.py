from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db  # Import SQLAlchemy instance from the app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class Repository(ABC):
    """Abstract base class defining the interface for data persistence operations."""
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based implementation of the Repository interface."""
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()

# --- SPECIFIC REPOSITORIES ---
class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific operations."""
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.model.query.filter_by(email=email).first()

class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place-specific operations."""
    def __init__(self):
        super().__init__(Place)

class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review-specific operations."""
    def __init__(self):
        super().__init__(Review)

class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity-specific operations."""
    def __init__(self):
        super().__init__(Amenity)
