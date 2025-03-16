import os
from datetime import timedelta

class Config:
    """Base configuration class with common settings"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Fallback secret key
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')  # Change in production
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SECRET_KEY = "dev-secret-key"  # Development-only secret key
    JWT_SECRET_KEY = "dev-super-secret-key"  # Dev JWT secret
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class ProductionConfig(Config):
    """Production environment configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'prod-super-secret-key')  # Production secret
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///production.db')

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-super-secret-key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests

# Configuration registry
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
