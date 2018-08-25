from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.article import ArticleDataAccess
from data_access.app_user import AppUserDataAccess
from data_access.article_group import ArticleGroupDataAccess
from view_models.article import ArticleModel
from decorators.general import rest_method
from decorators.security import requires_authentication, requires_role, get_claim_data

class ArticleController(Resource):
    @rest_method
    def get(self, article_id=None):
        # just a shell
        return None
    
    @rest_method
    def post(self):
        article_data = request.get_json()
        article = ArticleModel(**article_data)
        result = ArticleDataAccess().create_article(article)
        user = AppUserDataAccess().get_user_by_id(result.app_user_id)
        article_group = ArticleGroupDataAccess().get_article_group(result.article_group_id) if result.article_group_id is not None else None
        return ArticleModel._construct_for_output(result, user, article_group)