from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from datetime import datetime

'''
Importing necessary modules:
- Flask-RESTX components for API structure
- Flask request object for handling HTTP requests
- JWT utilities for authentication
- Facade service for business logic
- Datetime for timestamp handling
'''

api = Namespace('places', description='Place operations')

'''
Defining data models for API documentation and validation:
- Amenity model
- User model
- Place model (for input)
- Detailed Place model (for output, including relationships)
- Review model
'''

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new place.
        Requires authentication.
        """
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        if not user:
            return {"message": "User not found"}, 400

        place_data = request.json
        try:
            place_obj = facade.create_place(place_data)
            return {
                "id": place_obj.id,
                "title": place_obj.title,
                "description": place_obj.description,
                "price": place_obj.price,
                "latitude": place_obj.latitude,
                "longitude": place_obj.longitude,
                "owner_id": place_obj.owner.id,
                "owner": {
                    "id": place_obj.owner.id,
                    "first_name": place_obj.owner.first_name,
                    "last_name": place_obj.owner.last_name,
                    "email": place_obj.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in place_obj.amenities]
            }, 201
        except ValueError as e:
            return {"message": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places, including owner and amenities information.
        """
        places = facade.get_all_places()
        result = []
        for p in places:
            result.append({
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner.id,
                "owner": {
                    "id": p.owner.id,
                    "first_name": p.owner.first_name,
                    "last_name": p.owner.last_name,
                    "email": p.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in p.amenities]
            })
        return result, 200

@api.route('/<string:place_id>')
@api.param('place_id', 'The Place identifier')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve details of a place by its ID.
        """
        p = facade.get_place(place_id)
        if not p:
            return {"message": "Place not found"}, 404

        return {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": p.price,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "owner_id": p.owner.id,
            "owner": {
                "id": p.owner.id,
                "first_name": p.owner.first_name,
                "last_name": p.owner.last_name,
                "email": p.owner.email
            },
            "amenities": [{"id": a.id, "name": a.name} for a in p.amenities]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """
        Update a place's information.
        Requires authentication.
        """
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        if not user:
            return {"message": "User not found"}, 400

        place_data = request.json
        try:
            updated = facade.update_place(place_id, place_data)
            if not updated:
                return {"message": "Place not found"}, 404
            return {
                "id": updated.id,
                "title": updated.title,
                "description": updated.description,
                "price": updated.price,
                "latitude": updated.latitude,
                "longitude": updated.longitude,
                "owner_id": updated.owner.id,
                "owner": {
                    "id": updated.owner.id,
                    "first_name": updated.owner.first_name,
                    "last_name": updated.owner.last_name,
                    "email": updated.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in updated.amenities]
            }, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Admin access required')
    @jwt_required()
    def delete(self, place_id):
        """
        Delete a place by ID.
        The owner of the place or an admin can delete it.
        Requires authentication.
        """
        current_user = get_jwt_identity()
        user = facade.get_user(current_user['id'])
        if not user:
            return {"error": "User not found"}, 400

        place_obj = facade.get_place(place_id)
        if not place_obj:
            return {"message": "Place not found"}, 404

        if not (user.is_admin or (place_obj.owner.id == current_user['id'])):
            return {"error": "Unauthorized action"}, 403

        success = facade.delete_place(place_id)
        if success:
            return {"message": "Place deleted successfully"}, 200
        else:
            return {"message": "Place not found"}, 404

@api.route('/<string:place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404

        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'created_at': review.created_at.isoformat() if isinstance(review.created_at, datetime) else str(review.created_at),
            'updated_at': review.updated_at.isoformat() if isinstance(review.updated_at, datetime) else str(review.updated_at)
        } for review in reviews], 200

'''
This combined code provides a comprehensive API for managing places, including:
- Creating, reading, updating, and deleting places
- Retrieving place details with associated amenities and owner information
- Managing reviews for places
- Implementing authentication and authorization for certain operations
'''
