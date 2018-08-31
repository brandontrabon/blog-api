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
        if article_id is None:
            article_list = ArticleDataAccess().get_article()
            return [ArticleModel._construct_for_output(article, article.app_user, article.article_group) for article in article_list]
        else:
            article = ArticleDataAccess().get_article(article_id)
            return ArticleModel._construct_for_output(article, article.app_user, article.article_group)
    
    @rest_method
    def post(self):
        article_data = request.get_json()
        article = ArticleModel(**article_data)
        result = ArticleDataAccess().create_article(article)
        user = AppUserDataAccess().get_user_by_id(result.app_user_id)
        article_group = ArticleGroupDataAccess().get_article_group(result.article_group_id) if result.article_group_id is not None else None
        return ArticleModel._construct_for_output(result, user, article_group)
    
    @rest_method
    def put(self, article_id):
        article_data = request.get_json()
        result = ArticleDataAccess().edit_article(article_id, article_data)
        user = AppUserDataAccess().get_user_by_id(result.app_user_id)
        article_group = ArticleGroupDataAccess().get_article_group(result.article_group_id) if result.article_group_id is not None else None
        return ArticleModel._construct_for_output(result, user, article_group)
    
    @rest_method
    def delete(self, article_id):
        delete_successful = ArticleDataAccess().delete_article(article_id)

        if delete_successful == True:
            return '', 204
        else:
            return 'Article ID {} not found'.format(article_id), 410