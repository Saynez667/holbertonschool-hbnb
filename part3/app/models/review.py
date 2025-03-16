from .base_model import BaseModel

class Review(BaseModel):
    """
    Class representing a review

    Attributes:
        text (str): Content of the review
        rating (int): Rating between 1 and 5
        user_id (str): ID of the user who wrote the review
        place_id (str): ID of the place being reviewed
        created_at (datetime): Timestamp when the review is created
        updated_at (datetime): Timestamp when the review is last updated
    """

    def __init__(self, text, rating, user_id, place_id, **kwargs):
        """
        Initialize a new review

        Args:
            text (str): Review content
            rating (int): Rating between 1 and 5
            user_id (str): ID of the user who wrote the review
            place_id (str): ID of the place being reviewed
        """
        super().__init__(**kwargs)

        # Validate input
        self.text = self._validate_string(text, "Text", 1000)
        self._rating = 0
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def _validate_string(self, value, field_name, max_length):
        """Validate that a string is not empty and does not exceed max length"""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

    @property
    def rating(self):
        """Get the rating value"""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating value with validation"""
        try:
            rating_value = int(value)
            if rating_value < 1 or rating_value > 5:
                raise ValueError("Rating must be between 1 and 5")
            self._rating = rating_value
        except (ValueError, TypeError):
            if isinstance(value, (int, float)) and (value < 1 or value > 5):
                raise ValueError("Rating must be between 1 and 5")
            raise ValueError("Rating must be a number between 1 and 5")

    def update(self, data):
        """Update the review attributes based on the provided dictionary"""
        if 'text' in data:
            self.text = self._validate_string(data['text'], "Text", 1000)
        if 'rating' in data:
            self.rating = data['rating']
        if 'user_id' in data:
            self.user_id = data['user_id']
        if 'place_id' in data:
            self.place_id = data['place_id']
        super().update(data)

    def to_dict(self):
        """Convert the review to a dictionary"""
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        })
        return review_dict
