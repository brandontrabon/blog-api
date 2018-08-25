from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.article_group import ArticleGroupDataAccess
from view_models.app_user import AppUserModel
from decorators.general import rest_method

class ArticleGroupArticleController(Resource):
    @rest_method
    def get(self, article_group_id):
        user_list = ArticleGroupDataAccess().get_articles_by_article_group(article_group_id)
        return [AppUserModel._construct(n) for n in user_list]