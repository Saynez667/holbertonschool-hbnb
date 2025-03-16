import os

'''
Importing the 'os' module to interact with the operating system,
particularly for accessing environment variables.
'''

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

'''
Base Config class:
- Sets a SECRET_KEY from an environment variable or uses a default value
- Sets DEBUG to False by default
'''

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
    ADMIN_SECRET = os.getenv("ADMIN_SECRET", "default-admin-secret")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''
DevelopmentConfig class (inherits from Config):
- Overrides DEBUG to True for development environment
- Sets additional configuration for SECRET_KEY and ADMIN_SECRET
- Configures SQLAlchemy settings for development database
'''

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "secret_test_key"

'''
TestConfig class:
- Sets TESTING to True for test environment
- Configures SQLAlchemy to use an in-memory SQLite database
- Sets a specific SECRET_KEY for testing
'''

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

'''
Configuration dictionary:
- Maps configuration names to their respective classes
- Both 'development' and 'default' point to DevelopmentConfig
'''
