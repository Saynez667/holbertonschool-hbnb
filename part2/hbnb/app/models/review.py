from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id, **kwargs):
        super().__init__(**kwargs)
        self.text = self._validate_string(text, "Text", 1000)
        self._rating = 0
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def _validate_string(self, value, field_name, max_length):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

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
            if isinstance(value, (int, float)) and (value < 1 or value > 5):
                raise ValueError("Rating must be between 1 and 5")
            raise ValueError("Rating must be a number between 1 and 5")

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
