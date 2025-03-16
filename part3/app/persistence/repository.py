from abc import ABC, abstractmethod
from app import db
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import uuid
from datetime import datetime

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

'''
Base class:
- Uses SQLAlchemy's declarative base
- Automatically generates table names from class names
'''

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

'''
BaseModel class:
- Abstract base for all database models
- Provides common fields: id, created_at, updated_at
- Uses UUID for id and automatically manages timestamps
'''

class Repository(ABC):
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
    def update(self, instance):
        pass

    @abstractmethod
    def delete(self, instance):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

'''
Repository abstract base class:
- Defines the interface for all repository classes
- Includes methods for CRUD operations and attribute-based retrieval
'''

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, instance):
        db.session.add(instance)
        db.session.commit()

    def get(self, id):
        return db.session.query(self.model).get(id)

    def get_all(self):
        return db.session.query(self.model).all()

    def update(self, instance):
        db.session.commit()

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return db.session.query(self.model).filter(getattr(self.model, attr_name) == attr_value).first()

'''
SQLAlchemyRepository class:
- Concrete implementation of Repository for SQLAlchemy
- Handles database operations using SQLAlchemy's session
'''

class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, instance):
        if instance.id in self._storage:
            self._storage[instance.id] = instance

    def delete(self, instance):
        if instance.id in self._storage:
            del self._storage[instance.id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

    def get_by_email(self, email):
        return self.get_by_attribute('email', email)

'''
InMemoryRepository class:
- Concrete implementation of Repository for in-memory storage
- Useful for testing or small-scale applications without a database
- Implements all Repository methods using a dictionary for storage
'''
