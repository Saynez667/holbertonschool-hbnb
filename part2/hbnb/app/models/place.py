from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=None, **kwargs):
        super().__init__(**kwargs)
        self.title = self._validate_string(title, "Title", 100)
        self.description = self._validate_string(description, "Description", 1000)
        self._price = 0
        self.price = price
        self._latitude = 0
        self.latitude = latitude
        self._longitude = 0
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities if amenities else []

    def _validate_string(self, value, field_name, max_length):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

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

    def update(self, data):
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