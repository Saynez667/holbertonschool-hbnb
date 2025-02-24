from flask import Blueprint
from flask_restx import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

# Ajoutez ici les namespaces et les ressources de l'API
