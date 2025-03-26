from app import db
from .base_model import BaseModel
from sqlalchemy import ForeignKey

class Review(BaseModel):
    """Class representing a review"""

    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Relationships
    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)

    def __init__(self, text, rating, user_id, place_id, **kwargs):
        """Initialize a new review"""
        super().__init__(**kwargs)

        self.validate_text(text)
        self.validate_rating(rating)

        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @staticmethod
    def validate_text(text):
        """Validate review content"""
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating):
        """Validate rating"""
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        """Convert review to dictionary"""
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        return review_dict
