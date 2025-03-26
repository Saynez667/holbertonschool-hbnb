from app.extensions import db, bcrypt
from .base_model import BaseModel
import re

class User(BaseModel):
    """Represents a user in the system with SQLAlchemy integration."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        super().__init__(**kwargs)

        self.validate_first_name(first_name)
        self.validate_last_name(last_name)
        self.validate_email(email)
        self.validate_password(password)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email.lower()
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password using bcrypt."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify password hash."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return user_dict

    @staticmethod
    def validate_first_name(first_name):
        if not first_name or first_name.strip() == "":
            raise ValueError("First name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or less")

    @staticmethod
    def validate_last_name(last_name):
        if not last_name or last_name.strip() == "":
            raise ValueError("Last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or less")

    @staticmethod
    def validate_email(email):
        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_password(password):
        if not password or password.strip() == "":
            raise ValueError("Password cannot be empty")
