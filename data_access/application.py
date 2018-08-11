from sqlalchemy.sql import update, and_
from data_access.data_access_base import DataAccessBase
from data_models.models_raw import Application

class ApplicationDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_application_by_name(self, application_name):
        q = self.default_query(Application)
        q = q.filter(Application.application_name == application_name)

        return self.get_single_object_or_404(q, Application, application_name)

    def get_application_by_id(self, application_id):
        q = self.default_query(Application)
        q = q.filter(Application.application_id == application_id)

        return self.get_single_object_or_404(q, Application, application_id)