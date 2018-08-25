from sqlalchemy.sql import update, and_
from data_access.data_access_base import DataAccessBase
from data_access.application import ApplicationDataAccess
from data_access.role import RoleDataAccess
from data_access.claim import ClaimDataAccess
from data_models.models_raw import AppUser, AppUserApplication, AppUserAppRole, AppRole, AppClaim, AppUserAppClaim
from exceptions.http_exceptions import HttpNotFoundException

FIRST_NAME = 'firstname'
LAST_NAME = 'lastname'
PHONE_NUMBER = 'phonenumber'
EMAIL = 'email'
USERNAME = 'username'
IS_RESTRICTED = 'is_restricted'

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
    
    def get_roles_by_user_id(self, app_user_id):
        q = (
            self.default_query(AppRole)
            .join(AppUserAppRole)
            .filter(AppUserAppRole.app_user_id == app_user_id)
        )
        data = q.all()
        roles = [item.role_name for item in data]

        return roles

    def get_claim_data_by_user_id(self, app_user_id, claim_name):
        q = (
            self.default_query(AppUserAppClaim)
            .join(AppClaim)
            .filter(AppUserAppClaim.app_user_id == app_user_id)
            .filter(AppClaim.claim_name == claim_name)
        )

        user_claim = self.get_single_object_or_404(q, AppUserAppClaim, app_user_id)
        return user_claim.claim_value

    def create_user(self, user_payload, hashed_password):
        firstname = user_payload.get(FIRST_NAME)
        lastname = user_payload.get(LAST_NAME)
        phonenumber = user_payload.get(PHONE_NUMBER)
        email = user_payload.get(EMAIL)
        username = user_payload.get(USERNAME)
        is_restricted = False

        application = ApplicationDataAccess().get_application_by_name('Melinda\'s Blog')
        role = RoleDataAccess().get_role_by_name('VIEWER')
        claim = ClaimDataAccess().get_claim_by_name('RESTRICTED_ARTICLE_ACCESS')

        user = AppUser(
            firstname = firstname,
            lastname = lastname,
            phonenumber = phonenumber,
            email = email,
            username = username,
            password_hash = hashed_password,
            is_restricted = is_restricted
        )

        appUserApplication = AppUserApplication(
            app_user = user,
            application = application
        )

        appUserAppRole = AppUserAppRole(
            app_user = user,
            app_role = role
        )

        appUserAppClaim = AppUserAppClaim(
            app_user = user,
            app_claim = claim
        )

        self.session.add(user)
        self.session.add(appUserApplication)
        self.session.add(appUserAppRole)
        self.session.add(appUserAppClaim)
        self.session_commit_with_rollback()
        return user
    
    def create_admin_user(self, user_payload, hashed_password):
        firstname = user_payload.get(FIRST_NAME)
        lastname = user_payload.get(LAST_NAME)
        phonenumber = user_payload.get(PHONE_NUMBER)
        email = user_payload.get(EMAIL)
        username = user_payload.get(USERNAME)

        application = ApplicationDataAccess().get_application_by_name('Melinda\'s Blog')
        role = RoleDataAccess().get_role_by_name('ADMIN')
        claim = ClaimDataAccess().get_claim_by_name('RESTRICTED_ARTICLE_ACCESS')

        user = AppUser (
            firstname = firstname,
            lastname = lastname,
            phonenumber = phonenumber,
            email = email,
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

        appUserAppClaim = AppUserAppClaim(
            app_user = user,
            app_claim = claim
        )

        self.session.add(user)
        self.session.add(appUserApplication)
        self.session.add(appUserAppRole)
        self.session.add(appUserAppClaim)
        self.session_commit_with_rollback()
        return user
    
    def edit_user(self, app_user_id, app_user_payload):
        self.object_exists_or_404(AppUser.app_user_id == app_user_id, AppUser, app_user_id)

        app_user = self.get_user_by_id(app_user_id)
        app_user.firstname = app_user_payload.get(FIRST_NAME)
        app_user.lastname = app_user_payload.get(LAST_NAME)
        app_user.phonenumber = app_user_payload.get(PHONE_NUMBER)
        app_user.email = app_user_payload.get(EMAIL)
        app_user.is_restricted = app_user_payload.get(IS_RESTRICTED)

        self.session.add(app_user)
        self.session_commit_with_rollback()
        return app_user