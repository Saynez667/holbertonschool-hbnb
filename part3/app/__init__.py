# Third-party imports
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize extensions outside factory function
jwt = JWTManager()  # Handles JWT authentication
db = SQLAlchemy()   # Database ORM instance

def create_app(config_class=Config):
    """Factory function to create and configure a Flask application instance."""
    
    # Create Flask core object
    app = Flask(__name__)
    
    # Load configuration from class
    app.config.from_object(config_class)
    
    # Security check: Ensure JWT secret is set
    if not app.config.get("JWT_SECRET_KEY"):
        app.config["JWT_SECRET_KEY"] = "dev-super-secret-key"  # TEMP - Change in production!
    
    # Initialize extensions with app context
    jwt.init_app(app)  #  Connect JWT to app
    db.init_app(app)   #  Connect database to app

    # Configure REST API documentation
    api = Api(
        app,
        version='1.0',
        title='HBNB API',
        description='HBNB Application API',
        doc='/api/v1/'  #  Swagger UI endpoint
    )

    # Import API route groups (namespaces)
    from .api.v1.users import api as users_ns       #  User management endpoints
    from .api.v1.amenities import api as amenities_ns  #  Amenity resources
    from .api.v1.places import api as places_ns     #  Property listings
    from .api.v1.reviews import api as reviews_ns   #  Guest reviews
    from .api.v1.auth import api as auth_ns         #  Authentication routes

    # Register API endpoints
    api.add_namespace(users_ns, path='/api/v1/users')      # User routes
    api.add_namespace(amenities_ns, path='/api/v1/amenities')  # Amenity routes
    api.add_namespace(places_ns, path='/api/v1/places')    #  Property routes
    api.add_namespace(reviews_ns, path='/api/v1/reviews')  #  Review routes
    api.add_namespace(auth_ns, path='/api/v1/auth')        # Auth routes

    return app
