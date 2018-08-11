from flask_restful import abort, request

from security.authentication import Authentication
from exceptions.http_exceptions import HttpAuthenticationException

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
        print(app_user_id)

        if hasattr(jwt_info, 'err'):
            raise HttpAuthenticationException(message=getattr(jwt_info, 'message'))
        
        response = func(*args, app_user_id=app_user_id, **kwargs)
        return response
    
    return requires_authentication_func