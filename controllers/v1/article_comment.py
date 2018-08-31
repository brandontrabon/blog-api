from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.article_comment import ArticleCommentDataAccess
from view_models.article_comment import ArticleCommentModel
from decorators.general import rest_method

class ArticleCommentController(Resource):
    @rest_method
    def get(self, article_id):
        article_comment_list = ArticleCommentDataAccess().get_article_comment_by_article(article_id)
        return [
            ArticleCommentModel._construct_for_output(
                article_comment,
                article_comment.app_user,
                article_comment.article,
                article_comment.parent
            ) for article_comment in article_comment_list]
    
    @rest_method
    def post(self):
        article_comment_data = request.get_json()
        article_comment = ArticleCommentModel(**article_comment_data)
        result = ArticleCommentDataAccess().create_article_comment(article_comment)
        return ArticleCommentModel._construct(result)
    
    @rest_method
    def put(self, article_comment_id):
        article_comment_data = request.get_json()
        article_comment = ArticleCommentModel(**article_comment_data)
        result = ArticleCommentDataAccess().edit_article_comment(article_comment_id, article_comment)
        return ArticleCommentModel._construct(result)