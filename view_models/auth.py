from flask_restful_swagger_2 import Schema
from common.schema_fields import SchemaFields

TOKEN = 'token'

class AuthModel(Schema):
    type = 'object'
    properties = {
        TOKEN: SchemaFields.STRING
    }

    @classmethod
    def _construct(cls, auth_jwt):
        data = {
            TOKEN: auth_jwt
        }

        return cls(**data)
        