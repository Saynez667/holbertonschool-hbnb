import unittest
from app import create_app, db
from app.models.user import User

class UserCreationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(first_name='John', last_name='Doe', email='David@shlomo.com', password='password')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(email='john@shlomo.com').first())

if __name__ == '__main__':
    unittest.main()
