from sqlalchemy.sql import update, and_
from datetime import datetime
from data_access.data_access_base import DataAccessBase
from data_models.models_raw import Tag
from exceptions.http_exceptions import HttpNotFoundException

class TagDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_tag(self, tag_id=None):
        if tag_id is not None:
            self.object_exists_or_404(Tag.tag_id == tag_id, Tag, tag_id)
        
        q = self.default_query(Tag)

        if tag_id is not None:
            q = q.filter(Tag.tag_id == tag_id)
        
        if tag_id is not None:
            result = q.one_or_none()
        else:
            result = q.all()
        
        if result is None:
            raise HttpNotFoundException(message='Tag does not exist')
        
        return result
    
    def create_tag(self, tag_payload):
        tag = Tag(
            tag_name = tag_payload.get('tag_name')
        )

        self.session.add(tag)
        self.session_commit_with_rollback()
        return tag
    
    def edit_tag(self, tag_id, tag_payload):
        self.object_exists_or_404(Tag.tag_id == tag_id, Tag, tag_id)

        tag = self.get_tag(tag_id)
        tag.tag_name = tag_payload.get('tag_name')

        self.session.add(tag)
        self.session_commit_with_rollback()
        return tag
    
    def delete_tag(self, tag_id):
        tag = self.get_tag(tag_id)
        
        self.session.delete(tag)
        self.session_commit_with_rollback()
        return '', 204