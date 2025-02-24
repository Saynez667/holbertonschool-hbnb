from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, name, description, price_per_night, number_rooms, number_bathrooms, max_guests, latitude, longitude, address, owner):
        super().__init__()
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.number_rooms = number_rooms
        self.number_bathrooms = number_bathrooms
        self.max_guests = max_guests
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.owner = owner
        self.reviews = [] 
        self.amenities = []
        self.availability = True 

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Removes an amenity from the place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def get_average_rating(self):
         """Calculates the average rating based on reviews."""
         if not self.reviews:
            return 0.0 
         total_rating = sum(review.rating for review in self.reviews)
         return total_rating / len(self.reviews)

    def update_availability(self, available):
        """Updates the availability status of the place."""
        self.availability = available

    def calculate_total_price(self, number_of_nights):
        """Calculates the total price based on the number of nights."""
        return self.price_per_night * number_of_nights
