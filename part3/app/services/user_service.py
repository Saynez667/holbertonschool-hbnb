from app.persistence.database import db

def update_user(user, data):
    """Met à jour les informations d'un utilisateur"""
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.session.commit()
    return user