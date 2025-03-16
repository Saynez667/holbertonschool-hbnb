from app.models.place import Place
from app.persistence.database import db

def create_place(data):
    """Crée un nouveau lieu dans la base de données"""
    place = Place(**data)
    db.session.add(place)
    db.session.commit()
    return place

def update_place(place, data):
    """Met à jour un lieu existant"""
    for key, value in data.items():
        if hasattr(place, key):
            setattr(place, key, value)
    
    db.session.commit()
    return place

def delete_place(place):
    """Supprime un lieu de la base de données"""
    db.session.delete(place)
    db.session.commit()