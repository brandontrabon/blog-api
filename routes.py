from controllers.v1.article_group import ArticleGroupController
from controllers.v1.app_user import AppUserController
from controllers.v1.auth import AuthController

def setup_v1_routes(api):
    api.add_resource(ArticleGroupController, '/api/v1/article_group/<int:article_group_id>', '/api/v1/article_group')
    api.add_resource(AppUserController, '/api/v1/user/<int:app_user_id>', '/api/v1/user')
    api.add_resource(AuthController, '/api/v1/auth')

def setup_routes(api):
    setup_v1_routes(api)