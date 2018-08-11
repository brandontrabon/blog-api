import jwt
from datetime import datetime
import base64
import hashlib
import bcrypt

from data_access.app_user import AppUserDataAccess
from exceptions.http_exceptions import HttpAuthenticationException

from settings import JWT_PUBLIC_KEY, JWT_PRIVATE_KEY, JWT_EXPIRATION_TIMESPAN, API_KEY_EXPIRATION_TIMESPAN

class Authentication:
    def __init__(self):
        pass
    
    def hash_password(self, password):
        password_bytes = password.encode('utf-8')
        weak_hashed_password = base64.b64encode(hashlib.sha256(password_bytes).digest())
        salt = bcrypt.gensalt(rounds=12)
        password_bcrypt = bcrypt.hashpw(weak_hashed_password, salt)
        return password_bcrypt.decode('utf-8')

    def compare_passwords(self, password, encrypted_password):
        password_bytes = password.encode('utf-8')
        hashed_password = base64.b64encode(hashlib.sha256(password_bytes).digest())
        encrypted_password_bytes = encrypted_password.encode('utf-8')
        return bcrypt.checkpw(hashed_password, encrypted_password_bytes)

    def create_jwt(self, username, ip_address):
        payload = {
            'exp': datetime.utcnow() + JWT_EXPIRATION_TIMESPAN,
            'iat': datetime.utcnow(),
            'username': username,
            'ip_address': ip_address
        }

        return jwt.encode(payload, JWT_PRIVATE_KEY, algorithm='RS256').decode('utf-8')

    def decode_jwt(self, jwt_string):
        jwt_string = jwt_string.replace('Bearer ', '')
        try:
            return jwt.decode(jwt_string, JWT_PUBLIC_KEY, algorithms=['RS256'])
        except jwt.ExpiredSignatureError:
            return HttpAuthenticationException(message='JWT authentication failed: The user token is expired')
        except jwt.DecodeError:
            return HttpAuthenticationException(message='JWT authentication failed: Failed signature validation')
        except jwt.InvalidTokenError:
            return HttpAuthenticationException(message='JWT authentication failed')
    
    def authenticate_with_jwt(self, jwt_string, ip_address):
        payload = self.decode_jwt(jwt_string)

        if hasattr(payload, 'err'):
            return payload

        username = payload.get('username', None)
        previous_ip = payload.get('ip_address', None)
        token_expiration = payload.get('exp', None)

        if username is None or previous_ip is None or token_expiration is None:
            return HttpAuthenticationException(message='Invalid authentication token format')
        
        # may want to check the ip address to make sure it hasn't changed
        app_user = AppUserDataAccess().get_user_by_username(username)
        app_user_id = app_user.app_user_id

        return jwt_string, app_user_id