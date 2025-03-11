from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from datetime import datetime

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            review_data = api.payload
            new_review = facade.create_review(review_data)
            
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id,
                'created_at': new_review.created_at.isoformat() if isinstance(new_review.created_at, datetime) else str(new_review.created_at),
                'updated_at': new_review.updated_at.isoformat() if isinstance(new_review.updated_at, datetime) else str(new_review.updated_at)
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'created_at': review.created_at.isoformat() if isinstance(review.created_at, datetime) else str(review.created_at),
            'updated_at': review.updated_at.isoformat() if isinstance(review.updated_at, datetime) else str(review.updated_at)
        } for review in reviews], 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat() if isinstance(review.created_at, datetime) else str(review.created_at),
            'updated_at': review.updated_at.isoformat() if isinstance(review.updated_at, datetime) else str(review.updated_at)
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            
            if not updated_review:
                return {'error': 'Review not found'}, 404
                
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at.isoformat() if isinstance(updated_review.created_at, datetime) else str(updated_review.created_at),
                'updated_at': updated_review.updated_at.isoformat() if isinstance(updated_review.updated_at, datetime) else str(updated_review.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200

