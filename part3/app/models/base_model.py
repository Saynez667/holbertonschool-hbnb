from app import db
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

#Base = declarative_base() # Définir Base en dehors de la classe

class BaseModel(db.Model):
    """Base class for all models"""

    __abstract__ = True  # Indique que c'est une classe abstraite

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization"""
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def __repr__(self):
        """String representation of the model"""
        return f"<{self.__class__.__name__} id={self.id}>"
