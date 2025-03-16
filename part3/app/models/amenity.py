from .base_model import BaseModel

class Amenity(BaseModel):
    """
    Class representing an amenity
    """

    def __init__(self, name: str):
        """
        Initialize a new amenity
        Args:
            name (str): Name of the amenity
        """
        super().__init__()
        self.name = self._validate_name(name)
        self.places = []  # List of places with this amenity

    def _validate_name(self, name):
        """
        Validate the name of the amenity
        Args:
            name (str): The name to validate
        Returns:
            str: The validated name
        Raises:
            ValueError: If the name is not a non-empty string or exceeds 50 characters
        """
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Amenity name is required and must be a non-empty string")
        if len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters long")
        return name

    def update(self, data):
        """
        Update the amenity's attributes
        Args:
            data (dict): Data to update the amenity
        """
        if 'name' in data:
            data['name'] = self._validate_name(data['name'])
        super().update(data)

    def add_place(self, place):
        """
        Add a place associated with this amenity
        Args:
            place (object): The place to add
        """
        if place not in self.places:
            self.places.append(place)
            place.add_amenity(self)

    def to_dict(self):
        """
        Convert the amenity to a dictionary
        Returns:
            dict: Dictionary representation of the amenity
        """
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict
