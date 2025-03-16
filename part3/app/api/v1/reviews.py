from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from datetime import datetime

'''
Importing necessary modules:
- Flask-RESTX components for API structure and documentation
- Flask request object for handling HTTP requests
- JWT utilities for authentication and user identity management
- Facade service for business logic operations
- Datetime for handling timestamps in responses
'''

api = Namespace('reviews', description='Review operations')

'''
Defining the review model for input validation and documentation:
- Includes fields such as text, rating, user_id, and place_id
'''

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(description='ID of the user (optional, only set by backend)')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new review.
        Requires authentication.
        """
        current_user = get_jwt_identity()
        data = request.json
        data['user_id'] = current_user["id"]

        try:
            review_obj = facade.create_review(data)
            return {
                "id": review_obj.id,
                "text": review_obj.text,
                "rating": review_obj.rating,
                "user_id": review_obj.user.id,
                "place_id": review_obj.place.id,
                "created_at": review_obj.created_at.isoformat() if isinstance(review_obj.created_at, datetime) else str(review_obj.created_at),
                "updated_at": review_obj.updated_at.isoformat() if isinstance(review_obj.updated_at, datetime) else str(review_obj.updated_at)
            }, 201
        except Exception as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.
        """
        reviews = facade.get_all_reviews()
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id,
                "place_id": r.place.id,
                "created_at": r.created_at.isoformat() if isinstance(r.created_at, datetime) else str(r.created_at),
                "updated_at": r.updated_at.isoformat() if isinstance(r.updated_at, datetime) else str(r.updated_at)
            }
            for r in reviews
        ], 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Retrieve review details by ID.
        """
        review_obj = facade.get_review(review_id)
        if not review_obj:
            return {'message': 'Review not found'}, 404

        return {
            "id": review_obj.id,
            "text": review_obj.text,
            "rating": review_obj.rating,
            "user_id": review_obj.user.id,
            "place_id": review_obj.place.id,
            "created_at": review_obj.created_at.isoformat() if isinstance(review_obj.created_at, datetime) else str(review_obj.created_at),
            "updated_at": review_obj.updated_at.isoformat() if isinstance(review_obj.updated_at, datetime) else str(review_obj.updated_at)
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """
        Update a review's information.
        Requires authentication.
        """
        current_user = get_jwt_identity()
        review_obj = facade.get_review(review_id)
        if not review_obj:
            return {'message': 'Review not found'}, 404

        is_admin = current_user.get('is_admin', False)
        if not (is_admin or review_obj.user.id == current_user["id"]):
            return {'message': 'Unauthorized action'}, 403

        data = request.json
        try:
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'message': 'Review not found'}, 404

            return {
                "id": updated_review.id,
                "text": updated_review.text,
                "rating": updated_review.rating,
                "user_id": updated_review.user.id,
                "place_id": updated_review.place.id,
                "created_at": updated_review.created_at.isoformat() if isinstance(updated_review.created_at, datetime) else str(updated_review.created_at),
                "updated_at": updated_review.updated_at.isoformat() if isinstance(updated_review.updated_at, datetime) else str(updated_review.updated_at)
            }, 200
        except Exception as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete a review.
        Requires authentication.
        """
        current_user = get_jwt_identity()
        review_obj = facade.get_review(review_id)
        if not review_obj:
            return {'message': 'Review not found'}, 404

        is_admin = current_user.get('is_admin', False)
        if not (is_admin or review_obj.user.id == current_user["id"]):
            return {'message': 'Unauthorized action'}, 403

        success = facade.delete_review(review_id)
        if success:
            return {'message': 'Review deleted successfully'}, 200
        return {'message': 'Review not found'}, 404
