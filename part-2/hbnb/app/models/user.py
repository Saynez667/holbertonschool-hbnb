# models/user.py
import uuid
from datetime import datetime
import re

class User:
    """
    Represents a user in the system.
    """
    def __init__(self, first_name, last_name, email, is_admin=False):

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        """Getter for the first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Setter for the first name.  Must be a string <= 50 characters."""
        if not isinstance(value, str):
            raise TypeError("First name must be a string.")
        if len(value) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        self._first_name = value

    @property
    def last_name(self):
        """Getter for the last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Setter for the last name.  Must be a string <= 50 characters."""
        if not isinstance(value, str):
            raise TypeError("Last name must be a string.")
        if len(value) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        self._last_name = value

    @property
    def email(self):
        """Getter for the email address."""
        return self._email

    @email.setter
    def email(self, value):
        """Setter for the email address.  Must be a string and a valid email format."""
        if not isinstance(value, str):
            raise TypeError("Email must be a string.")
        if not self.is_valid_email(value):
            raise ValueError("Invalid email format.")
        self._email = value

    def is_valid_email(self, email):
        """
        Validates the email format using a simple regex.
        """
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Updates the attributes of the object based on the provided dictionary.
        """
        for key, value in data.items():	
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def __repr__(self):
        """
        Returns a string representation of the User instance.
        """
        return f"<User id={self.id}, email={self.email}>"
