from emissary import api
from emissary import custom_fields

from flask_restplus import Resource, fields


@api.route('/newb')
class NewbHandler(Resource):

    def get(self):
        return {'hola': 'fackoff'}

"""
EMAIL_MODEL = api.model('Email', {
    'to': custom_fields.Email(required=True),
    'to_name': fields.String(required=True),
    'from': custom_fields.Email(required=True),
    'from_name': fields.String(required=True),
    'subject': fields.String(required=True),
    'body': fields.String(required=True),
})
"""

EMAIL_MODEL = api.model('Email', {
    'no': fields.String(required=True),
})


RESPONSE_MODEL = api.model('Email Response', {
    'message': fields.String(required=True),
    'provider': fields.String(required=True),
})



@api.route('/email')
class Email(Resource):


    ###@api.response(400, 'watman')


    @api.marshal_with(RESPONSE_MODEL)
    @api.expect(EMAIL_MODEL, validate=True)
    def get(self):
        #return "damnit, janet!", 200
        return {'message': 'this is a sample message', 'provider': 'Mandrill'}






