from .base_model import BaseModel


class Amenity(BaseModel):

    def __init__(self, name, description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.places = [] 

    def update_amenity(self, new_name=None, new_description=None):
        """
        Updates the amenity's name and/or description.
        """
        if new_name:
            self.name = new_name
        if new_description:
            self.description = new_description

    def get_places(self):
        """
        Returns the list of places associated with this amenity.s.
        """
        return self.places
