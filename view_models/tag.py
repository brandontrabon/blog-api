from flask_restful_swagger_2 import Schema
from common.schema_fields import SchemaFields

TAG_ID = 'tag_id'
TAG_NAME = 'tag_name'

class TagModel(Schema):
    type = 'object'
    properties = {
        TAG_ID: SchemaFields.INT32,
        TAG_NAME: SchemaFields.STRING
    }

    @classmethod
    def _construct(cls, tag_obj):
        data = {
            TAG_ID: tag_obj.tag_id,
            TAG_NAME: tag_obj.tag_name
        }

        return cls(**data)