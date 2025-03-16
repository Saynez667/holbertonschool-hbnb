from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

'''
Importing necessary modules and extensions:
- Flask: Core framework for building the application.
- Flask-RESTx: For creating RESTful APIs with namespaces.
- Flask-Bcrypt: For password hashing.
- Flask-JWT-Extended: For token-based authentication.
- Flask-SQLAlchemy: For database ORM.
- API namespaces for modular organization of endpoints.
'''

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

'''
Application Factory Function:
- Creates and configures the Flask app instance.
- Registers extensions and API namespaces.
'''

def create_app(config_class=None):
    '''
    Initialize the Flask application and configure it.
    If a configuration class is provided, use it; otherwise, default settings are applied.
    '''
    app = Flask(__name__)
    
    # Example of setting a default configuration if none is provided
    if config_class:
        app.config.from_object(config_class)
    
    '''
    Initialize extensions with the application instance.
    '''
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    '''
    Set up the API with versioning and documentation.
    '''
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'  # Swagger documentation endpoint
    )

    '''
    Register namespaces for different resources:
    - Users, Amenities, Places, Reviews, and Authentication.
    Each namespace corresponds to a specific module in the application.
    '''
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
