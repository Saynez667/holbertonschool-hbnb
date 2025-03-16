from datetime import datetime
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest
from app.services.facade import facade
from app.api.v1.decorators import admin_required

api = Namespace('users', description='User operations')

# User model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description="First name of the user, max 50 characters",
        min_length=1,
        max_length=50,
        example='Lejoe'
    ),
    'last_name': fields.String(
        required=True,
        description="Last name of the user, max 50 characters",
        min_length=1,
        max_length=50,
        example='David'
    ),
    'email': fields.String(
        required=True,
        description="Email of the user, must be in valid format",
        pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        example='Lejoe.david@example.com'
    ),
    'password': fields.String(
        required=True,
        description="User password (hashed before storing)",
        min_length=6,
        example='DavidLacalotte123!'
    ),
    'is_admin': fields.Boolean(
        required=False,
        default=False,
        description="Admin status, defaults to False",
        example=False
    )
})

# User response model (excludes password for security reasons)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description="User unique identifier"),
    'first_name': fields.String(description="First name of the user"),
    'last_name': fields.String(description="Last name of the user"),
    'email': fields.String(description="Email of the user"),
    'is_admin': fields.Boolean(description="Admin status"),
    'created_at': fields.DateTime(description="Timestamp of user creation"),
    'updated_at': fields.DateTime(description="Timestamp of last update")
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model, mask=False)
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return users

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201, mask=False)
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @admin_required()
    def post(self):
        """Create a new user"""
        data = api.payload

        if 'password' not in data or not data['password'].strip():
            api.abort(400, "Password is required.")

        if 'is_admin' not in data:
            data['is_admin'] = False

        existing_user = facade.get_user_by_email(data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            user = facade.create_user(data)
            return user, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model, mask=False)
    def get(self, user_id):
        """Retrieve user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, mask=False)
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @admin_required()
    def put(self, user_id):
        """Update user details"""
        try:
            updated_user = facade.update_user(user_id, api.payload)
            if not updated_user:
                api.abort(404, 'User not found')
            return updated_user
        except ValueError as e:
            api.abort(400, str(e))
