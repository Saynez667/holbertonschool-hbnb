from flask_restx import Namespace, Resource, fields
from flask import request
from hbnb.business_logic.facade import HBNBFacade

ns = Namespace('amenities', description='Amenity operations')
facade = HBNBFacade()

amenity_model = ns.model('Amenity', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True)
})

@ns.route('/')
class AmenityList(Resource):
    @ns.doc('list_amenities')
    @ns.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        return facade.list_amenities()

    @ns.doc('create_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        return facade.create_amenity(**ns.payload), 201

@ns.route('/<string:id>')
@ns.response(404, 'Amenity not found')
@ns.param('id', 'The amenity identifier')
class Amenity(Resource):
    @ns.doc('get_amenity')
    @ns.marshal_with(amenity_model)
    def get(self, id):
        """Fetch an amenity given its identifier"""
        amenity = facade.get_amenity(id)
        if amenity:
            return amenity
        ns.abort(404, f"Amenity {id} doesn't exist")

    @ns.doc('update_amenity')
    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, id):
        """Update an amenity given its identifier"""
        amenity = facade.update_amenity(id, **ns.payload)
        if amenity:
            return amenity
        ns.abort(404, f"Amenity {id} doesn't exist")
