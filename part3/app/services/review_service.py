from app.models.review import Review
from app.persistence.database import db

def create_review(data):
    """Crée un nouvel avis dans la base de données"""
    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return review

def update_review(review, data):
    """Met à jour un avis existant"""
    for key, value in data.items():
        if hasattr(review, key):
            setattr(review, key, value)
    
    db.session.commit()
    return review

def delete_review(review):
    """Supprime un avis de la base de données"""
    db.session.delete(review)
    db.session.commit()