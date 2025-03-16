from uuid import uuid4
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.repository import SQLAlchemyRepository  # type: ignore
from app.persistence.repository import InMemoryRepository  # For in-memory storage
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Facade:
    def __init__(self, use_memory=False):
        """Initialize repositories based on storage type (SQL or in-memory)."""
        repo_class = InMemoryRepository if use_memory else SQLAlchemyRepository

        self.user_repository = repo_class(User)
        self.place_repository = repo_class(Place)
        self.amenity_repository = repo_class(Amenity)
        self.review_repository = repo_class(Review)

    # User Management
    def create_user(self, user_data):
        """Create a new user with password hashing."""
        if 'password' not in user_data or not user_data['password']:
            raise ValueError("Password is required")

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        user.hash_password(user_data['password'])

        return self.user_repository.add(user)

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repository.get_all()

    def update_user(self, user_id, data):
        if 'password' in data and data['password']:
            data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        return self.user_repository.update(user_id, data)

    # Amenity Management
    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            raise ValueError("Name is required")

        amenity = Amenity(name=amenity_data['name'])
        return self.amenity_repository.add(amenity)

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        if 'name' in amenity_data and not amenity_data['name'].strip():
            raise ValueError("Name is required and cannot be empty")
        return self.amenity_repository.update(amenity_id, amenity_data)

    # Place Management
    def create_place(self, place_data):
        if not place_data.get('title'):
            raise ValueError("Title is required")

        owner_id = place_data.get('owner_id')
        if not owner_id or not self.get_user(owner_id):
            raise ValueError(f"Owner with ID {owner_id} does not exist")

        if 'price' in place_data and float(place_data['price']) < 0:
            raise ValueError("Price cannot be negative")

        place = Place(
            title=place_data.get('title', 'Untitled'),
            description=place_data.get('description', ''),
            price=float(place_data.get('price', 0.0)),
            latitude=float(place_data.get('latitude', 0.0)),
            longitude=float(place_data.get('longitude', 0.0)),
            owner_id=owner_id
        )

        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.amenities.append(amenity)

        return self.place_repository.add(place)

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        if 'price' in place_data and float(place_data['price']) < 0:
            raise ValueError("Price cannot be negative")

        if 'latitude' in place_data and not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("Latitude must be between -90 and 90")

        if 'longitude' in place_data and not -180 <= float(place_data['longitude']) <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        if 'owner_id' in place_data and not self.get_user(place_data['owner_id']):
            raise ValueError(f"Owner with ID {place_data['owner_id']} does not exist")

        return self.place_repository.update(place_id, place_data)

    def get_place_with_details(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None

        owner = self.get_user(place.owner_id)
        amenities = [self.get_amenity(aid) for aid in place.amenities]
        reviews = self.get_reviews_by_place(place_id)

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner,
            'amenities': amenities,
            'reviews': reviews
        }

    # Review Management
    def create_review(self, review_data):
        if not self.get_user(review_data.get('user_id')):
            raise ValueError("User does not exist")
        if not self.get_place(review_data.get('place_id')):
            raise ValueError("Place does not exist")

        review = Review(
            text=review_data.get('text', ''),
            rating=review_data.get('rating', 0),
            user_id=review_data.get('user_id'),
            place_id=review_data.get('place_id')
        )

        return self.review_repository.add(review)

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        if not self.get_place(place_id):
            return []
        return self.review_repository.get_by_attribute('place_id', place_id)
