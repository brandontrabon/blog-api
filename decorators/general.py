from flask_restful import abort, request
from exceptions.http_exceptions import HttpStatusException

def rest_method(func):
    """
    Used to handle errors being thrown from rest calls
    """
    def format_error_message(error):
        return 'Error: {}'.format(error)

    def rest_method_func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpStatusException as se:
            abort(se.status_code, message=format_error_message(se), errors=se.errors)
        except Exception as e:
            abort(500, message=format_error_message(e))
        
    return rest_method_func_wrapper