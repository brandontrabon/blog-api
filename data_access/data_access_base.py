from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import exists
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from settings import DATABASE_URI
from exceptions.http_exceptions import HttpServerException, HttpNotFoundException

class DataAccessBase:
    session = None

    @staticmethod
    def initialize():
        """
        Performs initialization of the static variables
        """
        if DataAccessBase.session is None:
            DataAccessBase.session = scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=create_engine(DATABASE_URI))
            )
    
    def __init__(self):
        DataAccessBase.initialize()

    def default_query(self, query_object):
        """
        Returns the default query based upon the object being retrieved
        """
        return self.session.query(query_object)
    
    def session_commit_with_rollback(self, raises_server_exception=True):
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            if raises_server_exception:
                raise HttpServerException(e)
            return False
    
    def get_single_object_or_404(self, query_object, db_class, object_id):
        try:
            data = query_object.one()
            return data
        except (NoResultFound, MultipleResultsFound):
            raise HttpNotFoundException(message='{} ID {} does not exist'.format(db_class.__name__, object_id))
    
    def object_exists(self, exists_criteria):
        return self.session.query(exists().where(exists_criteria)).scalar()

    def object_exists_or_404(self, exists_criteria, db_class=None, object_id=None):
        if not self.object_exists(exists_criteria):
            if db_class is not None and object_id is not None:
                raise HttpNotFoundException(message='{} ID {} does not exist'.format(db_class.__name__, object_id))
            else:
                raise HttpNotFoundException(message='Requested object does not exist')
