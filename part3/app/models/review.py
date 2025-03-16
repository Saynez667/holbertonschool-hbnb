from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    '''
    Review class:
    - Inherits from BaseModel for common attributes and methods
    - Represents the 'reviews' table in the database
    - Includes relationships to User and Place models
    '''

    def __init__(self, text, rating, user, place, **kwargs):
        super().__init__(**kwargs)
        self.text = self._validate_string(text, "Text", 1000)
        self.rating = rating
        self.user_id = user.id if isinstance(user, db.Model) else user
        self.place_id = place.id if isinstance(place, db.Model) else place

    '''
    __init__ method:
    - Initializes a new Review instance
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
    - Validates string fields (text)
    - Ensures non-empty strings within specified length limits
    '''

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        try:
            rating_value = int(value)
            if rating_value < 1 or rating_value > 5:
                raise ValueError("Rating must be between 1 and 5")
            self._rating = rating_value
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5")

    '''
    rating property:
    - Implements getter and setter for the rating attribute
    - Ensures rating is an integer between 1 and 5
    '''

    def update(self, data):
        if 'text' in data:
            self.text = self._validate_string(data['text'], "Text", 1000)
        if 'rating' in data:
            self.rating = data['rating']
        if 'user_id' in data:
            self.user_id = data['user_id']
        if 'place_id' in data:
            self.place_id = data['place_id']
        super().update(data)

    '''
    update method:
    - Overrides BaseModel's update method
    - Implements specific validation for each field
    - Calls parent class's update method for common fields
    '''
