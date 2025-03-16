from app import db
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates
import re

class User(db.Model):
    """User model"""
    __tablename__ = 'users'  # Nom de la table

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<User id={self.id} email={self.email}>'

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name:
            raise ValueError('First name is required')
        if len(first_name) > 50:
            raise ValueError('First name must be at most 50 characters')
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name:
            raise ValueError('Last name is required')
        if len(last_name) > 50:
            raise ValueError('Last name must be at most 50 characters')
        return last_name

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email is required')
        if len(email) > 120:
            raise ValueError('Email must be at most 120 characters')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Invalid email format')
        return email
