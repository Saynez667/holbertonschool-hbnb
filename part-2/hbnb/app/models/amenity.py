# models/review.py
import uuid
from datetime import datetime
from models.place import Place
from models.user import User

class Review:
    """
    Represents a review for a place.
    """
    def __init__(self, text, rating, place, user):
        """
        Initializes a new Review instance.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """Getter for the text."""
        return self._text

    @text.setter
    def text(self, value):
        """Setter for the text.  Must be a string."""
        if not isinstance(value, str):
            raise TypeError("Text must be a string.")
        self._text = value

    @property
    def rating(self):
        """Getter for the rating."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Setter for the rating.  Must be an integer between 1 and 5."""
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer.")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        self._rating = value

    @property
    def place(self):
        """Getter for the place."""
        return self._place

    @place.setter
    def place(self, value):
        """Setter for the place.  Must be a Place instance."""
        if not isinstance(value, Place):
            raise TypeError("Place must be a Place instance.")
        self._place = value

    @property
    def user(self):
        """Getter for the user."""
        return self._user

    @user.setter
    def user(self, value):
        """Setter for the user.  Must be a User instance."""
        if not isinstance(value, User):
            raise TypeError("User must be a User instance.")
        self._user = value

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
        Returns a string representation of the Review instance.
        """
        return f"<Review id={self.id}, rating={self.rating}>"
