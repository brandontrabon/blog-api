from flask_restful_swagger_2 import Schema
from common.schema_fields import SchemaFields

APP_USER_ID = 'app_user_id'
USERNAME = 'username'
PASSWORD = 'password_hash'
IS_RESTRICTED = 'is_restricted'

class AppUserModel(Schema):
    type = 'object'
    properties = {
        APP_USER_ID: SchemaFields.INT32,
        USERNAME: SchemaFields.STRING,
        PASSWORD: SchemaFields.STRING,
        IS_RESTRICTED: SchemaFields.BOOLEAN
    }

    @classmethod
    def _construct(cls, app_user_object):
        data = {
            APP_USER_ID: app_user_object.app_user_id,
            USERNAME: app_user_object.username,
            PASSWORD: app_user_object.password_hash,
            IS_RESTRICTED: app_user_object.is_restricted
        }

        return cls(**data)
    