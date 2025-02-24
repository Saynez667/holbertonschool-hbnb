# hbnb/business_logic/facade.py

from hbnb.persistence.in_memory_repo import InMemoryRepo
from .user import User
from .place import Place
from .review import Review
from .amenity import Amenity

class HBNBFacade:
    def __init__(self):
        self.repo = InMemoryRepo()

    def create_user(self, **kwargs):
        return self.repo.create(User, **kwargs)

    def get_user(self, user_id):
        return self.repo.get(User, user_id)

    def update_user(self, user_id, **kwargs):
        user = self.get_user(user_id)
        if user:
            return self.repo.update(user, **kwargs)
        return None

    def delete_user(self, user_id):
        return self.repo.delete(User, user_id)

    def list_users(self):
        return self.repo.list(User)

    # Implémentez des méthodes similaires pour Place, Review et Amenity