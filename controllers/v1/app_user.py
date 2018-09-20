from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.app_user import AppUserDataAccess
from view_models.app_user import AppUserModel
from security.authentication import Authentication
from decorators.general import rest_method

class AppUserController(Resource):
    @rest_method
    def get(self, username):
        app_user = AppUserDataAccess().get_user_by_username(username)
        return AppUserModel._construct(app_user)

    @rest_method
    def post(self):
        app_user_data = request.get_json()

        # Add validation here

        # get the password and remove it from the object at the same time
        password = app_user_data.pop('password', None)
        hashed_password = Authentication().hash_password(password)
        app_user = AppUserModel(**app_user_data)
        # Only leave the admin user on when one needs to be created
        result = AppUserDataAccess().create_user(app_user, hashed_password)
        #result = AppUserDataAccess().create_admin_user(app_user, hashed_password)
        return AppUserModel._construct(result)
    