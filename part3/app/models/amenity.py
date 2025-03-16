from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    owner = db.relationship('User', backref='amenities', lazy=True)

    '''
    Amenity class:
    - Inherits from BaseModel for common attributes and methods
    - Represents the 'amenities' table in the database
    - Includes relationships to the User model via 'owner_id'
    '''

    def __init__(self, name, owner_id=None):
        super().__init__()

        '''
        __init__ method:
        - Initializes a new Amenity instance
        - Validates the 'name' attribute to ensure it is non-empty and ≤ 50 characters
        - Optionally assigns an 'owner_id' to establish ownership
        '''
        self.name = self._validate_name(name)
        self.owner_id = owner_id

    def _validate_name(self, name):
        """Validate the name of the amenity."""
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Amenity name is required and must be a non-empty string")
        if len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters long")
        return name
    
    '''
    _validate_name method:
    - Ensures the 'name' attribute is a non-empty string and ≤ 50 characters
    - Raises a ValueError if validation fails
    '''

    def update(self, data):
        """Update amenity attributes."""
        if 'name' in data:
            data['name'] = self._validate_name(data['name'])
        super().update(data)

    '''
    update method:
    - Overrides BaseModel's update method to include validation for the 'name' attribute
    - Calls the parent class's update method after validation
    '''
