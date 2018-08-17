from sqlalchemy.sql import update, and_
from data_access.data_access_base import DataAccessBase
from data_models.models_raw import AppClaim
from exceptions.http_exceptions import HttpNotFoundException

class ClaimDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_all_claims(self):
        q = self.default_query(AppClaim)
        return q.all()
    
    def get_claim_by_name(self, claim_name):
        q = self.default_query(AppClaim)
        q = q.filter(AppClaim.claim_name == claim_name)

        result = q.one_or_none()
        if result is None:
            raise HttpNotFoundException(message='Claim does not exist')

        return result