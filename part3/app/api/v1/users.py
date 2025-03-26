from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from werkzeug.exceptions import BadRequest

api = Namespace('users', description='User operations')

# Updated model with validation constraints
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', min_length=1, max_length=50, example='John'),
    'last_name': fields.String(required=True, description='Last name of the user', min_length=1, max_length=50, example='Doe'),
    'email': fields.String(required=True, description='Email of the user', pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', example='john.doe@example.com'),
    'password': fields.String(required=True, description='User password (hashed before storing)', min_length=6, example='SecurePassword123!'),
    'is_admin': fields.Boolean(required=False, default=False, description='Admin status, defaults to False', example=False)
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Timestamp of user creation'),
    'updated_at': fields.DateTime(description='Timestamp of last update')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model, mask=False)
    def get(self):
        """List all users"""
        return facade.get_users()

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, code=201, mask=False)
    @api.response(400, 'Validation Error')
    @jwt_required()  # ✅ Uniquement les admins peuvent créer un utilisateur
    def post(self):
        """Create a new user"""
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {'message': "Admin privileges required"}, 403

        data = api.payload

        if 'password' not in data or not data['password'].strip():
            api.abort(400, "Password is required.")

        try:
            user = facade.create_user(data)
            return user, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model, mask=False)
    def get(self, user_id):
        """Get a user by ID."""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, mask=False)
    @api.response(400, 'Validation Error')
    @jwt_required()
    def put(self, user_id):
        """Update a user (Admin can update anyone, users can only update themselves)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)

        # ✅ Un utilisateur ne peut modifier QUE son propre compte
        if not is_admin and current_user["id"] != user_id:
            return {'message': "Unauthorized action"}, 403

        user_data = api.payload

        # ✅ Empêcher les non-admins de modifier `email` et `password`
        if not is_admin and ("email" in user_data or "password" in user_data):
            return {'message': "You cannot modify email or password."}, 400

        try:
            user = facade.update_user(user_id, user_data)
            if not user:
                api.abort(404, f"User {user_id} not found")
            return user
        except ValueError as e:
            api.abort(400, str(e))
