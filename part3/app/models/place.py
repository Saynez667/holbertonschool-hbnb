from app import db
from app.models.base_model import BaseModel

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = db.relationship('User', backref='places', lazy=True)
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery', backref=db.backref('places', lazy=True))

    '''
    Place class:
    - Inherits from BaseModel for common attributes and methods
    - Represents the 'places' table in the database
    - Includes relationships to User (owner), Review, and Amenity models
    '''

    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None, **kwargs):
        super().__init__(**kwargs)
        self.title = self._validate_string(title, "Title", 100)
        self.description = self._validate_string(description, "Description", 1000)
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id if isinstance(owner, db.Model) else owner
        self.amenities = amenities if amenities else []

    '''
    __init__ method:
    - Initializes a new Place instance
    - Validates and sets all attributes
    - Handles both ORM and non-ORM initialization
    '''

    def _validate_string(self, value, field_name, max_length):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

    '''
    _validate_string method:
    - Validates string fields (title, description)
    - Ensures non-empty strings within specified length limits
    '''

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or value < -90 or value > 90:
            raise ValueError("Latitude must be a number between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or value < -180 or value > 180:
            raise ValueError("Longitude must be a number between -180 and 180")
        self._longitude = float(value)

    '''
    Property methods for price, latitude, and longitude:
    - Implement validation logic for these numeric fields
    - Ensure values are within acceptable ranges
    '''

    def update(self, data):
        for key, value in data.items():
            if key == 'title':
                self.title = self._validate_string(value, "Title", 100)
            elif key == 'description':
                self.description = self._validate_string(value, "Description", 1000)
            elif key in ['price', 'latitude', 'longitude']:
                setattr(self, key, value)
            elif key == 'owner_id':
                self.owner_id = value
            elif key == 'amenities':
                self.amenities = value
        super().update(data)

    '''
    update method:
    - Overrides BaseModel's update method
    - Implements specific validation for each field
    - Calls parent class's update method for common fields
    '''

    def add_review(self, review):
        """Adds a Review to the Place."""
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected 'review' to be an instance of Review.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an Amenity to the Place."""
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Expected 'amenity' to be an instance of Amenity.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    '''
    add_review and add_amenity methods:
    - Provide convenient ways to add related objects (reviews and amenities)
    - Include type checking to ensure correct object types are added
    '''
