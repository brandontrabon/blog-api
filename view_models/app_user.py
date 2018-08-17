from flask_restful_swagger_2 import Schema
from common.schema_fields import SchemaFields

APP_USER_ID = 'app_user_id'
FIRST_NAME = 'firstname'
LAST_NAME = 'lastname'
PHONE_NUMBER = 'phonenumber'
EMAIL = 'email'
USERNAME = 'username'
PASSWORD = 'password_hash'
IS_RESTRICTED = 'is_restricted'

class AppUserModel(Schema):
    type = 'object'
    properties = {
        APP_USER_ID: SchemaFields.INT32,
        FIRST_NAME: SchemaFields.STRING,
        LAST_NAME: SchemaFields.STRING,
        PHONE_NUMBER: SchemaFields.STRING,
        EMAIL: SchemaFields.STRING,
        USERNAME: SchemaFields.STRING,
        PASSWORD: SchemaFields.STRING,
        IS_RESTRICTED: SchemaFields.BOOLEAN
    }

    @classmethod
    def _construct(cls, app_user_object):
        data = {
            APP_USER_ID: app_user_object.app_user_id,
            FIRST_NAME: app_user_object.firstname,
            LAST_NAME: app_user_object.lastname,
            PHONE_NUMBER: app_user_object.phonenumber,
            EMAIL: app_user_object.email,
            USERNAME: app_user_object.username,
            PASSWORD: app_user_object.password_hash,
            IS_RESTRICTED: app_user_object.is_restricted
        }

        return cls(**data)
    