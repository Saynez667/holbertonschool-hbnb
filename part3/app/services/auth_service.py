import bcrypt

def verify_password(plain_password, hashed_password):
    """Vérifie si le mot de passe en clair correspond au hash stocké"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password):
    """Génère un hash sécurisé pour un mot de passe"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')