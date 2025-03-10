from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self._validate_string(first_name, "First name", 50)
        self.last_name = self._validate_string(last_name, "Last name", 50)
        self.email = self._validate_email(email)
        self.is_admin = is_admin

    def _validate_string(self, value, field_name, max_length):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

    def _validate_email(self, email):
        if not isinstance(email, str) or len(email.strip()) == 0:
            raise ValueError("Email is required and must be a non-empty string")
        email = email.strip().lower()
        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_regex.match(email):
            raise ValueError("Invalid email format")
        return email

    def update(self, data):
        if 'first_name' in data:
            self.first_name = self._validate_string(data['first_name'], "First name", 50)
        if 'last_name' in data:
            self.last_name = self._validate_string(data['last_name'], "Last name", 50)
        if 'email' in data:
            self.email = self._validate_email(data['email'])
        super().update(data)
