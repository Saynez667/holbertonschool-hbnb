from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self._validate_name(name)

    def _validate_name(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Amenity name is required and must be a non-empty string")
        if len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters long")
        return name

    def update(self, data):
        if 'name' in data:
            data['name'] = self._validate_name(data['name'])
        super().update(data)
