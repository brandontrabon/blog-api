from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.article_group import ArticleGroupDataAccess
from view_models.article_group import ArticleGroupModel
from decorators.general import rest_method
from decorators.security import requires_authentication

class ArticleGroupController(Resource):
    @rest_method
    @requires_authentication
    def get(self, article_group_id=None, app_user_id=None):
        #TODO: pass app_user_id to the user role decorator once it is created
        if article_group_id is None:
            article_group_list = ArticleGroupDataAccess().get_all_article_groups()
            return [ArticleGroupModel._construct(n) for n in article_group_list]
        else:
            article_group = ArticleGroupDataAccess().get_article_group(article_group_id)
            return ArticleGroupModel._construct(article_group)

    @rest_method
    def put(self, article_group_id):
        article_group_data = request.get_json()

        #Add validation here

        article_group = ArticleGroupModel(**article_group_data)
        result = ArticleGroupDataAccess().edit_article_group(article_group_id, article_group)
        return ArticleGroupModel._construct(result)

    @rest_method
    def post(self):
        article_group_data = request.get_json()
        article_group = ArticleGroupModel(**article_group_data)
        result = ArticleGroupDataAccess().create_article_group(article_group)
        return ArticleGroupModel._construct(result)

    @rest_method
    def delete(self, article_group_id):
        if ArticleGroupDataAccess().delete_article_group(article_group_id):
            return '', 204
        else:
            return 'Article Group ID {} not found'.format(article_group_id), 410