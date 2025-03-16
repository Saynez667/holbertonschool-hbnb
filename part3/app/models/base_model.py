from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    '''
    BaseModel class:
    - Inherits from db.Model to integrate with SQLAlchemy
    - Provides common attributes and methods for all models
    - Uses __abstract__ = True to prevent SQLAlchemy from creating a table for this base class
    '''
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    '''
    __init__ method:
    - Initializes a new instance with a unique ID and timestamps
    - This method is kept for compatibility with non-SQLAlchemy usage
    '''

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    '''
    save method:
    - Updates the 'updated_at' timestamp to the current time
    - Should be called whenever an object is modified and saved
    - Note: With SQLAlchemy, this might be redundant due to the 'onupdate' parameter in the column definition
    '''

    def update(self, data: dict):
        """
        Update object attributes from a dictionary.
        Also updates the 'updated_at' timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    '''
    update method:
    - Takes a dictionary of attributes to update
    - Updates only the attributes that exist in the object
    - Calls the save method to update the 'updated_at' timestamp
    - Provides a convenient way to update multiple attributes at once
    '''
