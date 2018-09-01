from controllers.v1.article_group import ArticleGroupController
from controllers.v1.article_group_article import ArticleGroupArticleController
from controllers.v1.article import ArticleController
from controllers.v1.app_user import AppUserController
from controllers.v1.tag import TagController
from controllers.v1.registration import RegistrationController
from controllers.v1.auth import AuthController

def setup_v1_routes(api):
    api.add_resource(ArticleGroupController, '/api/v1/article_groups/<int:article_group_id>', '/api/v1/article_groups')
    api.add_resource(ArticleGroupArticleController, '/api/v1/article_groups/<int:article_group_id>/articles')
    api.add_resource(ArticleController, '/api/v1/articles/<int:article_id>', '/api/v1/articles')
    api.add_resource(AppUserController, '/api/v1/users/<int:app_user_id>', '/api/v1/users')
    api.add_resource(TagController, '/api/v1/tags/<int:tag_id>', '/api/v1/tags')
    api.add_resource(RegistrationController, '/api/v1/auth/registration')
    api.add_resource(AuthController, '/api/v1/auth/login')

def setup_routes(api):
    setup_v1_routes(api)