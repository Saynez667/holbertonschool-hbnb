from datetime import datetime
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from app.api.v1.decorators import admin_required  # Import the decorator

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Expanded amenity model for responses
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier for the amenity'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.DateTime(description='Timestamp when the amenity was created'),
    'updated_at': fields.DateTime(description='Timestamp when the amenity was last updated'),
    'places': fields.List(fields.String(description='Place IDs with this amenity'))
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @admin_required()  # Protect the endpoint with admin privileges
    def post(self):
        """Create a new amenity"""
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat() if isinstance(new_amenity.created_at, datetime) else str(new_amenity.created_at),
                'updated_at': new_amenity.updated_at.isoformat() if isinstance(new_amenity.updated_at, datetime) else str(new_amenity.updated_at)
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
                'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
            } for amenity in amenities
        ], 200

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
                'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @admin_required()  # Protect the endpoint with admin privileges
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            amenity_data = api.payload
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
            return {'error': str(e)}, 400
        
