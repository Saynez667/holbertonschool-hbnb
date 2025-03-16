import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactivé pour toutes les configs

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'  # Spécifique à dev

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
