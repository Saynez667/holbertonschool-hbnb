class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = "your-default-secret-key"
    JWT_SECRET_KEY = "your-super-secret-key"

    # Common SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration with debugging and DB setup."""
    DEBUG = True
    SECRET_KEY = "dev-secret-key"
    JWT_SECRET_KEY = "dev-super-secret-key"
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost/hbnb_dev_db"

class TestingConfig(Config):
    """Testing configuration with SQLite in-memory DB."""
    TESTING = True
    SECRET_KEY = "test-secret-key"
    JWT_SECRET_KEY = "test-super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

class ProductionConfig(Config):
    """Production configuration (set strong secrets and proper DB URI)."""
    SECRET_KEY = "prod-secret-key"
    JWT_SECRET_KEY = "prod-super-secret-key"
    SQLALCHEMY_DATABASE_URI = "mysql://user:password@localhost/hbnb_prod_db"
