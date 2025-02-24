class HBNBFacade:
    def __init__(self):
        self.repo = InMemoryRepo()

    def create_user(self, **kwargs):
        return self.repo.create(User, **kwargs)

    def get_user(self, user_id):
        user = self.repo.get(User, user_id)
        if user:
            user_dict = user.__dict__.copy()
            user_dict.pop('password', None)
            return user_dict
        return None

    def update_user(self, user_id, **kwargs):
        user = self.repo.get(User, user_id)
        if user:
            kwargs.pop('password', None)  # Ne pas mettre à jour le mot de passe via cette méthode
            return self.repo.update(user, **kwargs)
        return None

    def list_users(self):
        users = self.repo.list(User)
        return [{k: v for k, v in user.__dict__.items() if k != 'password'} for user in users]
