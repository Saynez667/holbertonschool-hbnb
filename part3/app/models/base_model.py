from uuid import uuid4
from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base class for all models using SQLAlchemy"""
    __abstract__ = True  # Ensure SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save or update the instance in the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the instance from the database"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Update model attributes dynamically from keyword arguments"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        self.save()

    def to_dict(self):
        """Return dictionary representation of the instance"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def from_dict(cls, data):
        """Create an instance from a dictionary"""
        return cls(**data)
