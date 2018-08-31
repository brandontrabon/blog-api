from sqlalchemy.sql import update, and_
from datetime import datetime
from data_access.data_access_base import DataAccessBase
from data_models.models_raw import ArticleComment, Article
from exceptions.http_exceptions import HttpNotFoundException

class ArticleCommentDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_article_comment_by_id(self, article_comment_id):
        q = self.default_query(ArticleComment)
        q = q.filter(ArticleComment.article_comment_id == article_comment_id)
        result = q.one_or_none()

        if result is None:
            raise HttpNotFoundException(message='ArticleComment does not exist')

        return result
    
    def get_article_comment_by_article(self, article_id):
        q = (
            self.default_query(ArticleComment)
            .join(Article, and_(Article.article_id == article_id, ArticleComment.parent_id not None))
        )

        return q.all()
    
    def create_article_comment(self, article_comment_payload):
        article_comment = ArticleComment(
            article_id = article_comment_payload.get('article_id'),
            app_user_id = article_comment_payload.get('app_user_id'),
            parent_id = article_comment_payload.get('parent_id'),
            comment = article_comment_payload.get('comment'),
            is_flagged = article_comment_payload.get('is_flagged'),
            created_date = article_comment_payload.get('created_date'),
            updated_date = article_comment_payload.get('updated_date'),
            is_deleted = article_comment_payload.get('is_deleted')
        )

        self.session.add(article_comment)
        self.session_commit_with_rollback()
        return article_comment
    
    def edit_article_comment(self, article_comment_id, article_comment_payload):
        self.object_exists_or_404(ArticleComment.article_comment_id == article_comment_id, ArticleComment, article_comment_id)

        article_comment = self.get_article_comment_by_id(article_comment_id)
        article_comment.article_id = article_comment_payload.get('article_id')
        article_comment.app_user_id = article_comment_payload.get('app_user_id'),
        article_comment.parent_id = article_comment_payload.get('parent_id'),
        article_comment.comment = article_comment_payload.get('comment'),
        article_comment.is_flagged = article_comment_payload.get('is_flagged')
        article_comment.updated_date = datetime.utcnow()

        self.session.add(article_comment)
        self.session_commit_with_rollback()
        return article_comment