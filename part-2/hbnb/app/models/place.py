# models/place.py
import uuid
from datetime import datetime
from models.user import User  # Import for type hinting and validation

class Place:
    """
    Represents a place in the system.
    """
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initializes a new Place instance.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @property
    def title(self):
        """Getter for the title."""
        return self._title

    @title.setter
    def title(self, value):
        """Setter for the title.  Must be a string <= 100 characters."""
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters.")
        self._title = value

    @property
    def price(self):
        """Getter for the price."""
        return self._price

    @price.setter
    def price(self, value):
        """Setter for the price.  Must be a positive float or integer."""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
        if value <= 0:
            raise ValueError("Price must be a positive value.")
        self._price = value

    @property
    def latitude(self):
        """Getter for the latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Setter for the latitude.  Must be a float between -90.0 and 90.0."""
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float.")
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        self._latitude = value

    @property
    def longitude(self):
        """Getter for the longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Setter for the longitude.  Must be a float between -180.0 and 180.0."""
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float.")
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        self._longitude = value

    @property
    def owner(self):
        """Getter for the owner."""
        return self._owner

    @owner.setter
    def owner(self, value):
        """Setter for the owner.  Must be a User instance."""
        if not isinstance(value, User):
            raise TypeError("Owner must be a User instance.")
        self._owner = value

    def add_review(self, review):
        """
        Adds a review to the place.
        """
        from models.review import Review  # Import here to avoid circular dependency
        if not isinstance(review, Review):
            raise TypeError("Review must be a Review instance.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Adds an amenity to the place.
        """
        from models.amenity import Amenity  # Import here to avoid circular dependency
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an Amenity instance.")
        self.amenities.append(amenity)

    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Updates the attributes of the object based on the provided dictionary.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def __repr__(self):
        """
        Returns a string representation of the Place instance.
        """
        return f"<Place id={self.id}, title={self.title}>"
