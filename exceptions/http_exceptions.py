class HttpStatusException(Exception):
    DEFAULT_STATUS_CODE = 500

    def __init__(self, inner_exception=None, status_code=None, message=None, errors=None, *args, **kwargs):
        self._status_code = status_code
        self.message = message
        self.errors = errors
        if inner_exception is not None:
            self.inner_exception = inner_exception
        else:
            self.inner_exception = Exception(message)
        
        super().__init__(*args, **kwargs)
    
    @property
    def status_code(self):
        return self._status_code if self._status_code is not None else self.DEFAULT_STATUS_CODE

    def __str__(self):
        return '[{}]: {}'.format(self.status_code, self.inner_exception)

class HttpAuthenticationException(HttpStatusException):
    DEFAULT_STATUS_CODE = 401

    def __str__(self):
        return 'AuthenticationError {}'.format(super().__str__())

class HttpNotFoundException(HttpStatusException):
    DEFAULT_STATUS_CODE = 404

    def __str__(self):
        return 'ClientError {}'.format(super().__str__())

class HttpServerException(HttpStatusException):
    DEFAULT_STATUS_CODE = 500

    def __str__(self):
        return 'ServerError {}'.format(super().__str__())
