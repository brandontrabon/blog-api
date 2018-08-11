from flask_restful_swagger_2 import Schema
from common.schema_fields import SchemaFields

ARTICLE_GROUP_ID = 'article_group_id'
TITLE = 'title'
SHOW_ALL_LINKS = 'show_all_links'

class ArticleGroupModel(Schema):
    type = 'object'
    properties = {
        ARTICLE_GROUP_ID: SchemaFields.INT32,
        TITLE: SchemaFields.STRING,
        SHOW_ALL_LINKS: SchemaFields.BOOLEAN
    }

    @classmethod
    def _construct(cls, article_group_obj):
        data = {
            ARTICLE_GROUP_ID: article_group_obj.article_group_id,
            TITLE: article_group_obj.title,
            SHOW_ALL_LINKS: article_group_obj.show_all_links
        }

        return cls(**data)
