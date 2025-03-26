from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Modèle de requête pour la connexion
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Récupérer les données de la requête
        
        # Vérifier si l'utilisateur existe
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Générer un token JWT avec l'ID utilisateur et le rôle (admin ou non)
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        return {'access_token': access_token}, 200
