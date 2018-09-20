from flask_restful_swagger_2 import Schema
from common.schema_fields import SchemaFields

TOKEN = 'token'
ROLES = 'roles'

class AuthModel(Schema):
    type = 'object'
    properties = {
        TOKEN: SchemaFields.STRING,
        ROLES: SchemaFields.STRING_ARRAY
    }

    @classmethod
    def _construct(cls, auth_jwt, roles):
        data = {
            TOKEN: auth_jwt,
            ROLES: roles
        }

        return cls(**data)
        