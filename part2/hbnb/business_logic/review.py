# hbnb/business_logic/review.py

from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = kwargs.get('text', '')
        self.place_id = kwargs.get('place_id', '')
        self.user_id = kwargs.get('user_id', '')

# hbnb/business_logic/amenity.py

from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = kwargs.get('name', '')