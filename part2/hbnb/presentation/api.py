from flask_restx import Api, Resource, fields
from flask import request
from hbnb.business_logic.facade import HBNBFacade

api = Api(version='1.0', title='HBnB API')
ns = api.namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.String(readonly=True),
    'email': fields.String(required=True),
    'first_name': fields.String(),
    'last_name': fields.String(),
})

facade = HBNBFacade()

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return facade.list_users()

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        return facade.create_user(**api.payload), 201

@ns.route('/<string:id>')
@ns.response(404, 'User not found')
@ns.param('id', 'The user identifier')
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        """Fetch a user given its identifier"""
        user = facade.get_user(id)
        if user:
            return user
        api.abort(404, "User {} doesn't exist".format(id))

    @ns.doc('update_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, id):
        """Update a user given its identifier"""
        user = facade.update_user(id, **api.payload)
        if user:
            return user
        api.abort(404, "User {} doesn't exist".format(id))
