from app import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime

# Table d'association entre Place et Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.Integer, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(db.Model):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="places")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Place {self.id}: {self.title}>'

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title must be at most 100 characters long")
        return title

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError("Description is required")
        if len(description) > 1000:
            raise ValueError("Description must be at most 1000 characters long")
        return description

    @validates('price')
    def validate_price(self, key, price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        return float(price)

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        if not isinstance(latitude, (int, float)) or latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be a number between -90 and 90")
        return float(latitude)

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        if not isinstance(longitude, (int, float)) or longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be a number between -180 and 180")
        return float(longitude)
