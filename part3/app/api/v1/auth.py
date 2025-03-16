from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, create_refresh_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Login request model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Response model containing tokens and user info
token_response = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'user_id': fields.String(description='User ID'),
    'is_admin': fields.Boolean(description='Admin status')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_response, code=200)
    @api.response(400, 'Missing email or password')
    @api.response(401, 'Invalid email or password')
    def post(self):
        """
        Authenticate user and return JWT tokens
        
        This function handles user authentication:
        1. Validates the presence of email and password
        2. Retrieves the user from the database
        3. Verifies the password
        4. Generates access and refresh tokens
        5. Returns tokens along with user information
        """
        data = api.payload

        # Check if fields are provided
        if not data or not data.get('email') or not data.get('password'):
            api.abort(400, "Missing email or password")

        # Retrieve the user
        user = facade.get_user_by_email(data['email'])
        if not user or not user.verify_password(data['password']):
            api.abort(401, "Invalid email or password")

        # Add claims (admin role)
        additional_claims = {"is_admin": user.is_admin}

        # Generate tokens with additional claims
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=additional_claims)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": str(user.id),
            "is_admin": user.is_admin
        }
