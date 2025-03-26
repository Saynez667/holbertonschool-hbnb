from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Places management')

# Models for related entities (standardized names)
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity identifier'),
    'name': fields.String(description='Amenity name')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User identifier'),
    'first_name': fields.String(description='Owner first name'),
    'last_name': fields.String(description='Owner last name'),
    'email': fields.String(description='Owner email')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review identifier'),
    'text': fields.String(description='Review content'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User identifier')
})

# Model for creating a place
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title', min_length=1, max_length=100, example='Apartment with sea view'),
    'description': fields.String(required=False, description='Detailed place description', example='Beautiful apartment with sea view...'),
    'price': fields.Float(required=False, default=0.0, description='Price per night (positive value)', example=120.50),
    'latitude': fields.Float(required=False, default=0.0, description='Latitude (-90 to 90)', example=43.296482),
    'longitude': fields.Float(required=False, default=0.0, description='Longitude (-180 to 180)', example=5.369780),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs', example=['123e4567-e89b-12d3-a456-426614174000'])
})

# Detailed place model
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place unique identifier'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Place latitude'),
    'longitude': fields.Float(description='Place longitude'),
    'owner': fields.Nested(user_model, description='Place owner'),
    'amenities': fields.List(fields.Nested(amenity_model), description='Available amenities'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model, mask=False)
    def get(self):
        """Get list of all places"""
        return facade.get_places()

    @api.doc('create_place')
    @api.expect(place_model)
    @api.marshal_with(place_response_model, code=201, mask=False)
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()
        api.payload["owner_id"] = current_user["id"]
        
        try:
            return facade.create_place(api.payload), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>')
@api.param('place_id', 'Unique identifier for the place')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_response_model, mask=False)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if place is None:
            api.abort(404, f"Place {place_id} not found")
        return place

    @api.doc('update_place')
    @api.expect(place_model)
    @api.marshal_with(place_response_model, mask=False)
    @jwt_required()
    def put(self, place_id):
        """Update a place (Admins can modify any place)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)
        user_id = current_user.get("id")

        place = facade.get_place(place_id)
        if place is None:
            api.abort(404, f"Place {place_id} not found")

        # Admins can modify any place, users only their own
        if not is_admin and place["owner"]["id"] != user_id:
            api.abort(403, "Unauthorized action")

        try:
            return facade.update_place(place_id, api.payload), 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_place')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Admins can delete any place)"""
        current_user = get_jwt_identity()
        is_admin = current_user.get("is_admin", False)
        user_id = current_user.get("id")

        place = facade.get_place(place_id)
        if place is None:
            api.abort(404, f"Place {place_id} not found")

        # Admins can delete any place, users only their own
        if not is_admin and place["owner"]["id"] != user_id:
            api.abort(403, "Unauthorized action")

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200
