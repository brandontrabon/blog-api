from sqlalchemy.sql import update, and_
from data_access.data_access_base import DataAccessBase
from data_models.models_raw import ArticleGroup, Article
from exceptions.http_exceptions import HttpNotFoundException

class ArticleGroupDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_all_article_groups(self):
        q = self.default_query(ArticleGroup)
        q = q.filter(ArticleGroup.is_deleted == False)
        return q.all()

    def get_article_group(self, article_group_id):
        self.object_exists_or_404(ArticleGroup.article_group_id == article_group_id, ArticleGroup, article_group_id)
        q = self.default_query(ArticleGroup).filter(ArticleGroup.article_group_id == article_group_id)
        q = q.filter(ArticleGroup.is_deleted == False)
        
        result = q.one_or_none()
        if result is None:
            raise HttpNotFoundException(message='Article group does not exist')

        return result
    
    def get_articles_by_article_group(self, article_group_id):
        q = (
            self.default_query(Article)
            .join(ArticleGroup)
            .filter(ArticleGroup.article_group_id == article_group_id)
        )

        data = q.all()
        return data

    def edit_article_group(self, article_group_id, article_group_payload):
        article_group = self.get_article_group(article_group_id)
        article_group.title = article_group_payload.get('title')
        article_group.show_all_links = article_group_payload.get('show_all_links')

        self.session.add(article_group)
        self.session_commit_with_rollback()
        return article_group

    def create_article_group(self, article_group_payload):
        article_group = ArticleGroup(
            title = article_group_payload.get('title'),
            show_all_links = article_group_payload.get('show_all_links')
        )
        self.session.add(article_group)
        self.session_commit_with_rollback()
        return article_group

    def delete_article_group(self, article_group_id):
        self.object_exists_or_404(ArticleGroup.article_group_id == article_group_id, ArticleGroup, article_group_id)
        q = update(ArticleGroup.__table__)
        q = q.where(and_(ArticleGroup.article_group_id == article_group_id, ArticleGroup.is_deleted == False))
        q = q.values(is_deleted = True)
        article_group_result = self.session.execute(q)

        self.session_commit_with_rollback()
        return article_group_result.rowcount == 1
