from flask_restful_swagger_2 import Schema
from common import date_format
from common.schema_fields import SchemaFields
from view_models.app_user import AppUserModel
from view_models.article_group import ArticleGroupModel

ARTICLE_ID = 'article_id'
APP_USER_ID = 'app_user_id'
ARTICLE_GROUP_ID = 'article_group_id'
TITLE = 'title'
CONTENT = 'content'
DATE_TO_PUBLISH = 'date_to_publish'
PROMOTED_START_DATE = 'promoted_start_date'
PROMOTED_END_DATE = 'promoted_end_date'
COMMENTS_ENABLED = 'comments_enabled'
PRICE = 'price'
CREATED_DATE = 'created_date'
UPDATED_DATE = 'updated_date'
IS_DELETED = 'is_deleted'

APP_USER = 'app_user'
ARTICLE_GROUP = 'article_group'

class ArticleModel(Schema):
    type = 'object'
    properties = {
        ARTICLE_ID: SchemaFields.INT32,
        APP_USER_ID: SchemaFields.INT32,
        ARTICLE_GROUP_ID: SchemaFields.NULLABLE_INT32,
        TITLE: SchemaFields.STRING,
        CONTENT: SchemaFields.STRING,
        DATE_TO_PUBLISH: SchemaFields.DATETIME,
        PROMOTED_START_DATE: SchemaFields.DATETIME,
        PROMOTED_END_DATE: SchemaFields.DATETIME,
        COMMENTS_ENABLED: SchemaFields.BOOLEAN,
        PRICE: SchemaFields.NULLABLE_FLOAT,
        CREATED_DATE: SchemaFields.DATETIME,
        UPDATED_DATE: SchemaFields.DATETIME,
        IS_DELETED: SchemaFields.BOOLEAN,
        APP_USER: SchemaFields.OBJECT,
        ARTICLE_GROUP: SchemaFields.OBJECT
    }

    @classmethod
    def _construct(cls, article_obj):
        data = {
            ARTICLE_ID: article_obj.article_id,
            APP_USER_ID: article_obj.app_user_id,
            ARTICLE_GROUP_ID: article_obj.article_group_id,
            TITLE: article_obj.title,
            CONTENT: article_obj.content,
            DATE_TO_PUBLISH: article_obj.date_to_publish,
            PROMOTED_START_DATE: article_obj.promoted_start_date,
            PROMOTED_END_DATE: article_obj.promoted_end_date,
            COMMENTS_ENABLED: article_obj.comments_enabled,
            PRICE: article_obj.price,
            CREATED_DATE: article_obj.created_date,
            UPDATED_DATE: article_obj.updated_date,
            IS_DELETED: article_obj.is_deleted
        }

        return cls(**data)
    
    @classmethod
    def _construct_for_output(cls, article_obj, app_user_obj, article_group_obj=None):
        data = {
            ARTICLE_ID: article_obj.article_id,
            TITLE: article_obj.title,
            CONTENT: article_obj.content,
            DATE_TO_PUBLISH: date_format.get_iso_format_date_string(article_obj.date_to_publish) if article_obj.date_to_publish is not None else None,
            PROMOTED_START_DATE: date_format.get_iso_format_date_string(article_obj.promoted_start_date) if article_obj.promoted_start_date is not None else None,
            PROMOTED_END_DATE: date_format.get_iso_format_date_string(article_obj.promoted_end_date) if article_obj.promoted_end_date is not None else None,
            COMMENTS_ENABLED: article_obj.comments_enabled,
            PRICE: article_obj.price,
            CREATED_DATE: date_format.get_iso_format_date_string(article_obj.created_date) if article_obj.created_date is not None else None,
            UPDATED_DATE: date_format.get_iso_format_date_string(article_obj.updated_date) if article_obj.updated_date is not None else None,
            IS_DELETED: article_obj.is_deleted,
            APP_USER: AppUserModel._construct(app_user_obj),
            ARTICLE_GROUP: ArticleGroupModel._construct(article_group_obj) if article_group_obj is not None else None
        }

        return cls(**data)