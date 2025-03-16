import re
from app import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete')
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete')

    existing_emails = set()

    '''
    User class:
    - Inherits from BaseModel for common attributes and methods
    - Represents the 'users' table in the database
    - Includes relationships to Review and Place models
    - Implements email uniqueness check and password hashing
    '''

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = self._validate_string(first_name, "First name", 50)
        self.last_name = self._validate_string(last_name, "Last name", 50)
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.hash_password(password)

    '''
    __init__ method:
    - Initializes a new User instance
    - Validates and sets all attributes
    - Hashes the password before storing
    '''

    def _validate_string(self, value, field_name, max_length):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

    '''
    _validate_string method:
    - Validates string fields (first_name, last_name)
    - Ensures non-empty strings within specified length limits
    '''

    def _validate_email(self, email):
        if not isinstance(email, str) or len(email.strip()) == 0:
            raise ValueError("Email is required and must be a non-empty string")
        email = email.strip().lower()
        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_regex.match(email):
            raise ValueError("Invalid email format")
        if email in User.existing_emails:
            raise ValueError("This email is already in use.")
        User.existing_emails.add(email)
        return email

    '''
    _validate_email method:
    - Validates email format
    - Ensures email uniqueness
    '''

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the provided password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    '''
    Password methods:
    - hash_password: Securely hashes the password before storing
    - verify_password: Checks a given password against the stored hash
    '''

    def update(self, data):
        if 'first_name' in data:
            self.first_name = self._validate_string(data['first_name'], "First name", 50)
        if 'last_name' in data:
            self.last_name = self._validate_string(data['last_name'], "Last name", 50)
        if 'email' in data:
            self.email = self._validate_email(data['email'])
        if 'password' in data:
            self.hash_password(data['password'])
        super().update(data)

    '''
    update method:
    - Overrides BaseModel's update method
    - Implements specific validation for each field
    - Calls parent class's update method for common fields
    '''

    def to_dict(self):
        """Return a dictionary representation of the user (excluding the password)."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "places": [p.id for p in self.places],
            "reviews": [r.id for r in self.reviews],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    '''
    to_dict method:
    - Provides a dictionary representation of the user
    - Excludes sensitive information like password
    - Includes related places and reviews
    '''
