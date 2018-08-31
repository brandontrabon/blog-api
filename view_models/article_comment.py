from flask_restful_swagger_2 import Schema
from common import date_format
from common.schema_fields import SchemaFields
from view_models.app_user import AppUserModel
from view_models.article import ArticleModel

ARTICLE_COMMENT_ID = 'article_comment_id'
ARTICLE_ID = 'article_id'
APP_USER_ID = 'app_user_id'
PARENT_ID = 'parent_id'
COMMENT = 'comment'
IS_FLAGGED = 'is_flagged'
CREATED_DATE = 'created_date'
UPDATED_DATE = 'updated_date'
IS_DELETED = 'is_deleted'

APP_USER = 'app_user'
ARTICLE = 'article'
PARENT = 'parent'

class ArticleCommentModel(Schema):
    type = 'object'
    properties = {
        ARTICLE_COMMENT_ID: SchemaFields.INT32,
        ARTICLE_ID: SchemaFields.INT32,
        APP_USER_ID: SchemaFields.INT32,
        PARENT_ID: SchemaFields.NULLABLE_INT32,
        COMMENT: SchemaFields.STRING,
        IS_FLAGGED: SchemaFields.BOOLEAN,
        CREATED_DATE: SchemaFields.DATETIME,
        UPDATED_DATE: SchemaFields.DATETIME,
        IS_DELETED: SchemaFields.BOOLEAN,
        APP_USER: SchemaFields.OBJECT,
        ARTICLE: SchemaFields.OBJECT,
        PARENT: SchemaFields.OBJECT
    }

    @classmethod
    def _construct(cls, article_comment_obj):
        data = {
            ARTICLE_COMMENT_ID: article_comment_obj.article_comment_id,
            ARTICLE_ID: article_comment_obj.article_id,
            APP_USER_ID: article_comment_obj.app_user_id,
            PARENT_ID: article_comment_obj.parent_id,
            COMMENT: article_comment_obj.comment,
            IS_FLAGGED: article_comment_obj.is_flagged,
            CREATED_DATE: article_comment_obj.created_date,
            UPDATED_DATE: article_comment_obj.updated_date,
            IS_DELETED: article_comment_obj.is_deleted
        }

        return cls(**data)
    
    @classmethod
    def _construct_for_output(cls, article_comment_obj, app_user_obj, article_obj, parent_obj=None):
        data = {
            ARTICLE_COMMENT_ID: article_comment_obj.article_comment_id,
            ARTICLE_ID: article_comment_obj.article_id,
            APP_USER_ID: article_comment_obj.app_user_id,
            PARENT_ID: article_comment_obj.parent_id,
            COMMENT: article_comment_obj.comment,
            IS_FLAGGED: article_comment_obj.is_flagged,
            CREATED_DATE: article_comment_obj.created_date,
            UPDATED_DATE: article_comment_obj.updated_date,
            IS_DELETED: article_comment_obj.is_deleted,
            APP_USER: AppUserModel._construct(app_user_obj),
            ARTICLE: ArticleModel._construct(article_obj),
            PARENT: cls._construct(parent_obj) if parent_obj is not None else None
        }

        return cls(**data)