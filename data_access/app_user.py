from sqlalchemy.sql import update, and_
from data_access.data_access_base import DataAccessBase
from data_access.application import ApplicationDataAccess
from data_access.role import RoleDataAccess
from data_models.models_raw import AppUser, AppUserApplication, AppUserAppRole
from exceptions.http_exceptions import HttpNotFoundException

USERNAME = 'username'

class AppUserDataAccess(DataAccessBase):
    def __init__(self):
        super().__init__()
    
    def get_user_by_username(self, username):
        q = self.default_query(AppUser)
        q = q.filter(AppUser.username == username)

        return self.get_single_object_or_404(q, AppUser, username)

    def get_user_by_id(self, app_user_id):
        q = self.default_query(AppUser)
        q = q.filter(AppUser.app_user_id == app_user_id)

        return self.get_single_object_or_404(q, AppUser, app_user_id)

    def create_user(self, user_payload, hashed_password):
        username = user_payload.get(USERNAME)
        is_restricted = False

        # add the application/user association

        # assign roles and claims
    
    def create_admin_user(self, user_payload, hashed_password):
        username = user_payload.get(USERNAME)

        application = ApplicationDataAccess().get_application_by_name('Melindas Blog')
        role = RoleDataAccess().get_role_by_name('ADMIN')

        user = AppUser (
            username = username,
            password_hash = hashed_password,
            is_restricted = False
        )

        appUserApplication = AppUserApplication(
            app_user =  user,
            application = application
        )

        appUserAppRole = AppUserAppRole(
            app_user = user,
            app_role = role
        )

        self.session.add(appUserApplication)
        self.session.add(appUserAppRole)
        self.session_commit_with_rollback()
        return user