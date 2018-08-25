from flask_restful import abort, request

from security.authentication import Authentication
from exceptions.http_exceptions import HttpAuthenticationException
from data_access.app_user import AppUserDataAccess

def get_key_or_default(kwargs, key, default_value):
    return_value = default_value
    if key in kwargs:
        return_value = kwargs.pop(key)
    
    return return_value

def requires_authentication(func):
    """
    This decorator tells a route that a user must be authenticated to call it.
    """
    def requires_authentication_func(*args, **kwargs):
        jwt_string = request.headers.get('Authorization')

        if jwt_string is None:
            raise HttpAuthenticationException(message='Authorization header is missing')
        
        authentication = Authentication()
        jwt_info, app_user_id = authentication.authenticate_with_jwt(jwt_string, request.remote_addr)

        if hasattr(jwt_info, 'err'):
            raise HttpAuthenticationException(message=getattr(jwt_info, 'message'))
        
        decorator_data = get_key_or_default(kwargs, 'decorator_data', {})
        decorator_data['app_user_id'] = app_user_id
        response = func(*args, decorator_data=decorator_data, **kwargs)
        return response
    
    return requires_authentication_func

def requires_role(role_list):
    """
    Used to define the roles that are allowed to call a particular route
    """
    def requires_role_decorator(func):
        
        def requires_role_decorator_func(*args, **kwargs):
            decorator_data = get_key_or_default(kwargs, 'decorator_data', {})
            app_user_id = decorator_data['app_user_id']
            role_array = role_list.split(',')
            user_roles = AppUserDataAccess().get_roles_by_user_id(app_user_id)

            for user_role in user_roles:
                try:
                    role_index = role_array.index(user_role)
                    if role_index > -1:
                        return func(*args, decorator_data=decorator_data, **kwargs)
                except ValueError as ve:
                    raise HttpAuthenticationException(message='Access denied')
        
        return requires_role_decorator_func
    
    return requires_role_decorator

def get_claim_data(claim_name):

    def get_claim_data_decorator(func):

        def get_claim_data_decorator_func(*args, **kwargs):
            decorator_data = get_key_or_default(kwargs, 'decorator_data', {})
            app_user_id = decorator_data['app_user_id']
            claim_data = AppUserDataAccess().get_claim_data_by_user_id(app_user_id, claim_name)
            decorator_data['claim_name'] = claim_name
            decorator_data['claim_data'] = claim_data

            return func(*args, decorator_data=decorator_data, **kwargs)

        return get_claim_data_decorator_func

    return get_claim_data_decorator