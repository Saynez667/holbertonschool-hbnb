from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password ,is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password
        self.places = []  # List of Place objects - CRITICAL
        self.reviews = [] # List of Review objects - CRITICAL


    def create_place(self, place):
        """Creates a new place associated with the user."""
        self.places.append(place)
        return place # return the created place

    def update_profile(self, first_name=None, last_name=None, email=None, password=None):
        """Updates the user's profile information."""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        if password:
            self.password = password

    def get_reviews(self):
        """Retrieves the user's reviews."""
        return self.reviews

    def authenticate(self, email, password):
        """Authenticates the user by checking email and password."""
        return self.email == email and self.password == password
