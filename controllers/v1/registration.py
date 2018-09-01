from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.app_user import AppUserDataAccess
from view_models.app_user import AppUserModel
from security.authentication import Authentication
from exceptions.http_exceptions import HttpAuthenticationException
from decorators.general import rest_method

class RegistrationController(Resource):
    @rest_method
    def post(self):
        registration_data = request.get_json()

        # get the password and remove it from the object at the same time
        password = registration_data.pop('password', None)
        hashed_password = Authentication().hash_password(password)
        app_user = AppUserModel(**registration_data)
        result = AppUserDataAccess().create_user(app_user, hashed_password)
        model = AppUserModel._construct(result)
        model.pop('password_hash', None)
        return model