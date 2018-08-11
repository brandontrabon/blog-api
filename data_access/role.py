from sqlalchemy.sql import update, and_
from data_access.data_access_base import DataAccessBase
from data_models.models_raw import AppRole
from exceptions.http_exceptions import HttpNotFoundException

class RoleDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_all_roles(self):
        q = self.default_query(AppRole)
        return q.all()

    def get_role_by_name(self, role_name):
        q = self.default_query(AppRole)
        q = q.filter(AppRole.role_name == role_name)

        result = q.one_or_none()
        if result is None:
            raise HttpNotFoundException(message='Role does not exist')

        return result