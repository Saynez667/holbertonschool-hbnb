from datetime import datetime
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(description='Administrative privileges', default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload
            if 'is_admin' not in user_data:
                user_data['is_admin'] = False  # Ensure default value


            existing_user = facade.get_user_by_email(user_data['email'])
            if (existing_user):
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id, 
                'first_name': new_user.first_name, 
                'last_name': new_user.last_name, 
                'email': new_user.email,
                'is_admin': new_user.is_admin,
                'created_at': new_user.created_at.isoformat() if isinstance(new_user.created_at, datetime) else str(new_user.created_at),
                'updated_at': new_user.updated_at.isoformat() if isinstance(new_user.updated_at, datetime) else str(new_user.updated_at)
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'created_at': user.created_at.isoformat() if isinstance(user.created_at, datetime) else str(user.created_at),
            'updated_at': user.updated_at.isoformat() if isinstance(user.updated_at, datetime) else str(user.updated_at)
        } for user in users], 200

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat() if isinstance(user.created_at, datetime) else str(user.created_at),
            'updated_at': user.updated_at.isoformat() if isinstance(user.updated_at, datetime) else str(user.updated_at)
        }, 200

            
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        try:
            user_data = api.payload
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id, 
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name, 
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'created_at': updated_user.created_at.isoformat() if isinstance(updated_user.created_at, datetime) else str(updated_user.created_at),
                'updated_at': updated_user.updated_at.isoformat() if isinstance(updated_user.updated_at, datetime) else str(updated_user.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

