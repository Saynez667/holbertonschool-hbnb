from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

'''
Importing necessary modules:
- Namespace and Resource from Flask-RESTx for API structure
- Fields for defining the data models used in the API
- JWT utilities for authentication and user identity management
- Facade service to interact with the business logic layer
'''

api = Namespace('amenities', description='Amenity operations')

'''
Defining the Amenity model:
- Specifies the structure of an amenity object with a required "name" field
'''

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new amenity.
        Any authenticated user can create an amenity.
        """
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        if not user:
            return {'message': 'User not found'}, 400

        amenity_data = api.payload
        amenity_data["owner_id"] = user.id

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat() if isinstance(new_amenity.created_at, datetime) else str(new_amenity.created_at),
                'updated_at': new_amenity.updated_at.isoformat() if isinstance(new_amenity.updated_at, datetime) else str(new_amenity.updated_at)
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve all amenities.
        This endpoint is open to everyone.
        """
        amenities = facade.get_all_amenities()
        return [
            {
                'id': a.id,
                'name': a.name,
                'created_at': a.created_at.isoformat() if isinstance(a.created_at, datetime) else str(a.created_at),
                'updated_at': a.updated_at.isoformat() if isinstance(a.updated_at, datetime) else str(a.updated_at)
            }
            for a in amenities
        ], 200

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The Amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get details of an amenity by its ID.
        Open to everyone.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
            'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """
        Update an amenity's information.
        Any authenticated user can update an amenity.
        """
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        if not user:
            return {'message': 'User not found'}, 400

        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat() if isinstance(updated_amenity.created_at, datetime) else str(updated_amenity.created_at),
                'updated_at': updated_amenity.updated_at.isoformat() if isinstance(updated_amenity.updated_at, datetime) else str(updated_amenity.updated_at)
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin access required')
    @jwt_required()
    def delete(self, amenity_id):
        """
        Delete an amenity by ID.
        The owner of the amenity or an admin can delete it.
        """
        current_user = get_jwt_identity()
        user = facade.get_user(current_user["id"])
        if not user:
            return {"error": "User not found"}, 400

        # Retrieve the amenity to verify ownership or admin rights
        amenity_obj = facade.get_amenity(amenity_id)
        if not amenity_obj:
            return {"error": "Amenity not found"}, 404

        # Check if the user is admin or owner of the amenity
        if not (user.is_admin or amenity_obj.owner_id == user.id):
            return {"error": "Unauthorized action"}, 403

        success = facade.delete_amenity(amenity_id)
        if success:
            return {"message": "Amenity deleted successfully"}, 200
        else:
            return {"error": "Amenity not found"}, 404
