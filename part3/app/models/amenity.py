from app import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from app.models.associations import place_amenity

class Amenity(db.Model):
    """Amenity model"""
    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Amenity id={self.id} name={self.name}>'

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Amenity name is required')
        if len(name) > 50:
            raise ValueError('Amenity name must be at most 50 characters')
        return name
