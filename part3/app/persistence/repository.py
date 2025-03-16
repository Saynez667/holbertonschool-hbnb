from abc import ABC, abstractmethod
from app import db

class Repository(ABC):
    """Abstract base class defining the interface for data persistence operations.
    
    This class defines the contract that all repository implementations must follow,
    providing standard methods for CRUD operations on objects.
    """
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


class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface.
    
    This implementation stores objects in a dictionary that exists only for the 
    lifetime of the application. No data persistence between application restarts.
    """
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add an object to the in-memory storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Get all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object's data in the storage."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Remove an object from the storage."""
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Find an object by a specific attribute value."""
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

    def get_by_email(self, email):
        """Convenience method to find an object by email attribute."""
        return self.get_by_attribute('email', email)


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the Repository interface.
    
    This implementation uses SQLAlchemy ORM to persist data in a relational database.
    """
    def __init__(self, model_class):
        """Initialize the repository with the model class it will manage.
        
        Args:
            model_class: The SQLAlchemy model class this repository will handle
        """
        self.model_class = model_class

    def add(self, obj):
        """Add a new object to the database.
        
        Args:
            obj: The object to add to the database
        """
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get an object by its ID.
        
        Args:
            obj_id: The ID of the object to retrieve
            
        Returns:
            The object if found, None otherwise
        """
        return db.session.get(self.model_class, obj_id)

    def get_all(self):
        """Get all objects of this type from the database.
        
        Returns:
            A list of all objects
        """
        return db.session.query(self.model_class).all()

    def update(self, obj_id, data):
        """Update an object with new data.
        
        Args:
            obj_id: The ID of the object to update
            data: A dictionary of attributes to update
            
        Returns:
            The updated object if found, None otherwise
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object from the database.
        
        Args:
            obj_id: The ID of the object to delete
            
        Returns:
            True if the object was deleted, False otherwise
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute value.
        
        Args:
            attr_name: The name of the attribute to filter by
            attr_value: The value to search for
            
        Returns:
            The first matching object if found, None otherwise
        """
        return db.session.query(self.model_class).filter(
            getattr(self.model_class, attr_name) == attr_value
        ).first()
