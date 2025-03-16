from app.models.base_model import BaseModel
from .user import User

class Place(BaseModel):
    """Class representing a rental place

    Attributes:
        title (str): The title of the place (max 100 characters)
        description (str): Detailed description of the place
        price (float): Price per night (must be positive)
        latitude (float): Latitude coordinate (-90.0 to 90.0)
        longitude (float): Longitude coordinate (-180.0 to 180.0)
        owner (User): User instance of who owns the place
        amenities (list): List of amenities associated with the place
        reviews (list): List of reviews for the place
    """

    def __init__(self, title, owner, description="", price=0.0, latitude=0.0, longitude=0.0, amenities=None, **kwargs):
        """Initialize a new Place

        Args:
            title (str): Place title (required)
            owner (User): User instance of who owns the place
            description (str): Detailed description of the place
            price (float): Price per night
            latitude (float): Geographic latitude
            longitude (float): Geographic longitude
            amenities (list): List of amenities
        """
        super().__init__(**kwargs)

        self.title = self._validate_string(title, "Title", 100)
        self.validate_owner(owner)
        self.description = self._validate_string(description, "Description", 1000)
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = amenities if amenities else []
        self.reviews = []

    def _validate_string(self, value, field_name, max_length):
        """Validate string fields like title and description"""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

    @staticmethod
    def validate_owner(owner):
        """Validate that the owner is a User instance"""
        if not owner:
            raise ValueError("Place must have an owner")
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def update(self, data):
        """Update place attributes from a dictionary"""
        if 'title' in data:
            self.title = self._validate_string(data['title'], "Title", 100)
        if 'description' in data:
            self.description = self._validate_string(data['description'], "Description", 1000)
        if 'price' in data:
            self.price = data['price']
        if 'latitude' in data:
            self.latitude = data['latitude']
        if 'longitude' in data:
            self.longitude = data['longitude']
        if 'owner_id' in data:
            self.owner_id = data['owner_id']
        if 'amenities' in data:
            self.amenities = data['amenities']
        super().update(data)

    def to_dict(self):
        """Convert place to dictionary"""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if self.owner else None,
            'amenities': [amenity.id for amenity in self.amenities] if self.amenities else []
        })
        return place_dict
