from flask import Blueprint

# Define the Blueprint locally
bp = Blueprint('api', __name__)

# Avoid importing modules here to prevent circular imports
# These imports will be handled later inside the create_app() function