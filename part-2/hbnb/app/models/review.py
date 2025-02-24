from .base_model import BaseModel
from typing import Union

class Review(BaseModel):
    def __init__(self, user: str, place: str, text: str, rating: int):
        super().__init__()
        self.user = user
        self.place = place
        self.text = text
        self.rating = self.validate_rating(rating)

    def validate_rating(self, rating: int) -> int:
        """Validates that the rating is within a reasonable range."""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

    def update_review(self, text: str = None, rating: int = None):
        """Updates the review text and/or rating."""
        if text:
            self.text = text
        if rating:
            self.rating = self.validate_rating(rating)

    def delete_review(self):
        """Handles the deletion of the review."""
        print(f"Review deleted for place: {self.place} by user: {self.user}")
        pass
