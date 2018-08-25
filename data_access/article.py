from sqlalchemy.sql import update, and_
from datetime import datetime
from data_access.data_access_base import DataAccessBase
from data_models.models_raw import Article
from exceptions.http_exceptions import HttpNotFoundException

class ArticleDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_article(self, article_id=None):
        self.object_exists_or_404(Article.article_id == article_id, Article, article_id)

        q = self.default_query(Article)

        if article_id is not None:
            q = q.filter(Article.article_id == article_id)

        q = q.filter(Article.is_deleted == False)

        result = q.one_or_none()
        if result is None:
            raise HttpNotFoundException(message='Article does not exist')

        return result
    
    def create_article(self, article_payload):
        article = Article(
            app_user_id = article_payload.get('app_user_id'),
            article_group_id = article_payload.get('article_group_id'),
            title = article_payload.get('title'),
            content = article_payload.get('content'),
            date_to_publish = article_payload.get('date_to_publish'),
            promoted_start_date = article_payload.get('promoted_start_date'),
            promoted_end_date = article_payload.get('promoted_end_date'),
            comments_enabled = article_payload.get('comments_enabled'),
            price = article_payload.get('price')
        )

        self.session.add(article)
        self.session_commit_with_rollback()
        return article
    
    def edit_article(self, article_id, article_payload):
        self.object_exists_or_404(Article.article_id == article_id, Article, article_id)

        article = self.get_article(article_id)
        article.article_group_id = article_payload.get('article_group_id')
        article.title = article_payload.get('title')
        article.content = article_payload.get('content')
        article.date_to_publish = article_payload.get('date_to_publish')
        article.promoted_start_date = article_payload.get('promoted_start_date')
        article.promoted_end_date = article_payload.get('promoted_end_date')
        article.comments_enabled = article_payload.get('comments_enabled')
        article.price = article_payload.get('price')
        article.updated_date = article_payload.get('updated_date')

        self.session.add(article)
        self.session_commit_with_rollback()
        return article
    
    def delete_article(self, article_id):
        self.object_exists_or_404(Article.article_id == article_id, Article, article_id)

        q = update(Article.__table__)
        q = q.where(and_(Article.article_id == article_id, Article.is_deleted == False))
        q = q.values(is_deleted = True)

        article_result = self.session.execute(q)
        self.session_commit_with_rollback()
        return article_result.rowcount == 1