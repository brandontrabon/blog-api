from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.app_user import AppUserDataAccess
from view_models.app_user import AppUserModel
from view_models.auth import AuthModel
from security.authentication import Authentication
from exceptions.http_exceptions import HttpAuthenticationException
from decorators.general import rest_method

class AuthController(Resource):
    @rest_method
    def post(self):
        user_data = request.get_json()
        ip_address = request.remote_addr

        if not user_data or 'username' not in user_data or 'password' not in user_data:
            raise HttpAuthenticationException(message='Invalid Login')

        username = user_data.get('username')
        password = user_data.get('password')
        user = AppUserDataAccess().get_user_by_username(username)
        auth_obj = Authentication()
        if auth_obj.compare_passwords(password, user.password_hash) == False:
            raise HttpAuthenticationException(message='Invalid Login')
            
        auth_jwt = auth_obj.create_jwt(username, ip_address)
        return AuthModel._construct(auth_jwt)
