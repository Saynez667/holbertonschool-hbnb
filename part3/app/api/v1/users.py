from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from config import DevelopmentConfig

api = Namespace('users', description='User operations')

'''
Define the user model for input validation and documentation:
- Includes fields for user details and admin secret for special privileges
'''
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password'),
    'admin_secret': fields.String(required=False, description='Secret to create an admin account'),
    'is_admin': fields.Boolean(description='Administrative privileges', default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    def post(self):
        """
        Self-registration: Create a new user.
        """
        try:
            user_data = api.payload
            admin_secret = user_data.pop('admin_secret', None)
            if admin_secret and admin_secret == DevelopmentConfig.ADMIN_SECRET:
                user_data['is_admin'] = True
            else:
                user_data['is_admin'] = False

            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
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
    @jwt_required()
    def get(self):
        """
        Retrieve the list of all users. Requires admin privileges.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

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
        """
        Retrieve user details by ID.
        """
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
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """
        Update a user's own details or any user's details if admin.
        """
        current_user = get_jwt_identity()
        if current_user['id'] != user_id and not current_user.get('is_admin', False):
            return {'message': 'Unauthorized action'}, 403

        try:
            user_data = api.payload
            user_data.pop('admin_secret', None)
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

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, user_id):
        """
        Delete a user account. User can delete their own account or admin can delete any account.
        """
        current_user = get_jwt_identity()
        if current_user['id'] != user_id and not current_user.get('is_admin', False):
            return {'message': 'Unauthorized action'}, 403

        try:
            deleted_user = facade.delete_user(user_id)
            if not deleted_user:
                return {'error': 'User not found'}, 404
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            return {'error': f'Error deleting user: {str(e)}'}, 500

'''
This combined code provides a comprehensive API for user management, including:
- User registration with optional admin privileges
- Retrieving user details and list of all users (admin only)
- Updating user information (self or admin)
- Deleting user accounts (self or admin)
- JWT authentication for protected routes
- Proper error handling and response formatting
'''
