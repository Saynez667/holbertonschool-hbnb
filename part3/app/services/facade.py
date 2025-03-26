from flask_bcrypt import Bcrypt
from app.persistence.repository import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class Facade:
    def __init__(self):
        """Initialize repositories using SQLAlchemy."""
        self.user_repo = UserRepository()  
        self.place_repo = PlaceRepository()  
        self.review_repo = ReviewRepository()  
        self.amenity_repo = AmenityRepository()  
        self.bcrypt = Bcrypt()

    # --- USER OPERATIONS ---
    def create_user(self, user_data):
        """Create a new user with hashed password."""
        if 'password' not in user_data or not user_data['password'].strip():
            raise ValueError("Password is required.")
        
        # Hash password before storing
        user_data['password'] = self.bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_user_by_email(email)
    
    def get_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()
    
    def update_user(self, user_id, data):
        """Update user details."""
        return self.user_repo.update(user_id, data)
    
    def delete_user(self, user_id):
        """Delete a user."""
        self.user_repo.delete(user_id)

    # --- PLACE OPERATIONS ---
    def create_place(self, place_data):
        """Create a new place."""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)
    
    def get_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, data):
        """Update a place."""
        return self.place_repo.update(place_id, data)
    
    def delete_place(self, place_id):
        """Delete a place."""
        self.place_repo.delete(place_id)

    # --- AMENITY OPERATIONS ---
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, data):
        """Update an amenity."""
        return self.amenity_repo.update(amenity_id, data)
    
    def delete_amenity(self, amenity_id):
        """Delete an amenity."""
        self.amenity_repo.delete(amenity_id)

    # --- REVIEW OPERATIONS ---
    def create_review(self, review_data):
        """Create a new review."""
        review = Review(**review_data)
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()
    
    def update_review(self, review_id, data):
        """Update a review."""
        return self.review_repo.update(review_id, data)
    
    def delete_review(self, review_id):
        """Delete a review."""
        self.review_repo.delete(review_id)
