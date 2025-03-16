from app.persistence.repository import InMemoryRepository
from app.services.user_repository import UserRepository
from app.services.place_repository import PlaceRepository
from app.services.review_repository import ReviewRepository
from app.services.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from datetime import datetime

class HBnBFacade:
    def __init__(self):
        '''
        HBnBFacade constructor:
        - Initializes repositories for users, places, reviews, and amenities.
        - Chooses between InMemoryRepository (for testing) and SQLAlchemy repositories.
        '''
        self.user_repo = UserRepository()  # Use SQLAlchemy repository
        self.place_repo = PlaceRepository()  # Use SQLAlchemy repository
        self.review_repo = ReviewRepository()  # Use SQLAlchemy repository
        self.amenity_repo = AmenityRepository()  # Use SQLAlchemy repository
        # self.user_repo = InMemoryRepository() # => A decommenter pour inMemory
        # self.place_repo = InMemoryRepository()
        # self.review_repo = InMemoryRepository()
        # self.amenity_repo = InMemoryRepository()

    def _user_to_dict(self, user_obj):
        ''''
        Helper method to convert a User object to a dictionary.
        '''
        if not user_obj:
            return None
        return {
            "id": user_obj.id,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "email": user_obj.email,
            "is_admin": getattr(user_obj, 'is_admin', False)
        }

    def _amenity_to_dict(self, amenity_obj):
        ''''
        Helper method to convert an Amenity object to a dictionary.
        '''
        if not amenity_obj:
            return None
        return {
            "id": amenity_obj.id,
            "name": amenity_obj.name
        }

    def _place_to_dict(self, place_obj):
        ''''
        Helper method to convert a Place object to a dictionary.
        '''
        if not place_obj:
            return None
        return {
            "id": place_obj.id,
            "title": place_obj.title,
            "description": place_obj.description,
            "price": place_obj.price,
            "latitude": place_obj.latitude,
            "longitude": place_obj.longitude,
            "owner_id": place_obj.owner_id,
            "amenities": [a.id for a in place_obj.amenities] if hasattr(place_obj, "amenities") else []
        }

    def _review_to_dict(self, review_obj):
        ''''
        Helper method to convert a Review object to a dictionary.
        '''
        if not review_obj:
            return None
        return {
            "id": review_obj.id,
            "text": review_obj.text,
            "rating": review_obj.rating,
            "user_id": review_obj.user_id,
            "place_id": review_obj.place_id
        }

    # USERS
    def create_user(self, user_data):
        ''''
        Creates a new user:
        - Hashes the password
        - Adds the user to the repository
        '''
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        ''''
        Retrieves a user by ID.
        '''
        return self.user_repo.get(user_id)

    def get_user_by_id(self, user_id):  # utilisé dans admin_required()
        ''''
        Retrieves a user by ID (alias).
        '''
        return self.get_user(user_id)

    def get_user_by_email(self, email):
        ''''
        Retrieves a user by email.
        '''
        return self.user_repo.get_by_attribute( 'email', email)

    def get_all_users(self):
        ''''
        Retrieves all users and converts them to dictionaries.
        '''
        users = self.user_repo.get_all()
        return [self._user_to_dict(user) for user in users]

    def update_user(self, user_id, user_data):
        ''''
        Updates user information:
        - Handles password hashing if the password is being updated
        - Updates the user in the repository
        '''
        user = self.get_user(user_id)
        if user:
            if "password" in user_data:
                user.hash_password(user_data["password"])
                user_data.pop("password")
            for key, value in user_data.items():
                setattr(user, key, value)
            self.user_repo.update(user)
            return user
        return None

    def delete_user(self, user_id):
        ''''
        Deletes a user:
        - First deletes associated places and reviews
        - Then deletes the user from the repository
        '''
        user = self.get_user(user_id)
        if user:
            # Supprime d'abord les places et critiques associées
            for place in user.places:
                self.place_repo.delete(place)
            for review in user.reviews:
                self.review_repo.delete(review)

            # Puis supprime l'utilisateur
            self.user_repo.delete(user)
            return True
        return False

    # AMENITIES
    def create_amenity(self, amenity_data):
        ''''
        Creates a new amenity.
        '''
        name = amenity_data.get("name", "")
        if not name or len(name) > 50:
            raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
        owner_id = amenity_data.get("owner_id")
        amenity_obj = Amenity(name=name, owner_id=owner_id)
        self.amenity_repo.add(amenity_obj)
        return amenity_obj

    def get_amenity(self, amenity_id):
        ''''
        Retrieves an amenity by ID.
        '''
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        ''''
        Retrieves all amenities.
        '''
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        ''''
        Updates amenity information.
        '''
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        self.amenity_repo.add(amenity)
        return amenity

    def delete_amenity(self, amenity_id):
        ''''
        Deletes an amenity by ID.
        '''
        amenity = self.get_amenity(amenity_id)
        if amenity:
            self.amenity_repo.delete(amenity)
            return True
        return False

    # PLACES
    def create_place(self, place_data):
        ''''
        Creates a new place after validating owner and amenities.
        '''
        # Validate owner exists
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            error_msg = f"Owner with ID {owner_id} does not exist"
            raise ValueError(error_msg)

        # Validate amenities if provided
        if 'amenities' in place_data and place_data['amenities']:
            valid_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                valid_amenities.append(amenity_id)
            place_data['amenities'] = valid_amenities

        # Validate price
        if place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")

        # Validate latitude
        if not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")

        # Validate longitude
        if not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        # Create and save place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        ''''
        Retrieves a place by ID.
        '''
        return self.place_repo.get(place_id)

    def get_all_places(self):
        ''''
        Retrieves all places.
        '''
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        ''''
        Updates a place after validating related data.
        '''
        place = self.get_place(place_id)
        if not place:
            return None

        # Validate owner if changing
        if 'owner_id' in place_data:
            owner = self.get_user(place_data.get('owner_id'))
            if not owner:
                raise ValueError(f"Owner with ID {place_data.get('owner_id')} does not exist")

        # Validate amenities if changing
        if 'amenities' in place_data and place_data['amenities']:
            valid_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                valid_amenities.append(amenity_id)
            place_data['amenities'] = valid_amenities

        # Validate price
        if "price" in place_data and place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")

        # Validate latitude
        if "latitude" in place_data and not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")

        # Validate longitude
        if "longitude" in place_data and not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        
        # Update place
        #self.place_repo.update(place) # =>  A modifier si utilisation de inMemory
        self.place_repo.update(place_id, place_data) # ==>  A modifier si utilisation de inMemory
        return self.get_place(place_id)

    # REVIEWS
    def create_review(self, review_data):
        ''''
        Creates a new review after validating user_id, place_id, and rating.
        '''
        # Validate user exists
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")

        # Validate place exists
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")

        # Validate rating
        if not (1 <= review_data.get('rating') <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        
        # Create and save review
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        ''''
        Retrieves a review by ID.
        '''
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        ''''
        Retrieves all reviews.
        '''
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        '''
        Retrieves all reviews for a specific place.
        '''
        # First verify that the place exists
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Filter reviews by place_id
        all_reviews = self.get_all_reviews()
        return [review for review in all_reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        '''
        Updates a review after validation.
        '''
        review = self.get_review(review_id)
        if not review:
            return None

        # Validate user_id if it's being updated
        if 'user_id' in review_data:
            user = self.get_user(review_data.get('user_id'))
            if not user:
                raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")

        # Validate place_id if it's being updated
        if 'place_id' in review_data:
            place = self.get_place(review_data.get('place_id'))
            if not place:
                raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")

        # Validate rating
        if "rating" in review_data and not (1 <= review_data["rating"] <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        # Update review
        #self.review_repo.update(review) # =>  A modifier si utilisation de inMemory
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        ''''
        Deletes a review.
        '''
        review = self.get_review(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True

    def get_place_with_details(self, place_id):
        ''''
        Gets place with detailed info about owner, amenities and reviews details.
        '''
        place = self.get_place(place_id)
        if not place:
            return None

        # Get owner details
        owner = self.get_user(place.owner_id)
        owner_details = None
        if owner:
            owner_details = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            }

        # Get amenities details
        amenity_details = []
        if hasattr(place, 'amenities') and place.amenities:
            for amenity_id in place.amenities:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    amenity_details.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })

        # Get reviews details
        review_details = []
        reviews = self.get_reviews_by_place(place_id)
        if reviews:
            for review in reviews:
                review_details.append({
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                })

        # Create detailed response with all place info
        from datetime import datetime
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_details,
            'amenities': amenity_details,
            'reviews': review_details,
            'created_at': place.created_at.isoformat() if isinstance(place.created_at, datetime) else str(place.created_at),
            'updated_at': place.updated_at.isoformat() if isinstance(place.updated_at, datetime) else str(place.updated_at)
        }

facade = HBnBFacade()
