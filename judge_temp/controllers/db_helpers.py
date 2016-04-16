"""
This module is used for performing all database operations
required for the applications. It creates engine required for
db operations and also initializes sessionmaker for creating a session to
make transactions.

Attributes:
    engine (Engine): instance of .Engine class of sqlalchemy to work with database
    DBSession (Session): .Session class from sqlalchemy module with given configuration.
        Currently it only initializes it with bind=engine
    db_session (DBSession):  instance of DBSession() to perform transactions with database
"""

from .. import app, admin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base, User, Problem, Solution
from flask.ext.admin.contrib.sqla import ModelView

db_session_instance = None

engine = create_engine(app.config['DB_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine,expire_on_commit=False)

def get_db_session(create_new_instance=False):
    global db_session_instance
    if db_session_instance is None or create_new_instance:
        db_session = DBSession()
        db_session_instance = db_session
        db_session = db_session_instance
    else:
        db_session = db_session_instance
    return db_session


def insert_to_db(db_session, obj):
    """ Inserts object to required database

    Args:
        db_session (sessionmaker()): current database session of object
        obj (ModelClass): object of any model described
    """
    db_session.add(obj)
    db_session.commit()
    db_session.close()


class UserModelView(ModelView):
    column_display_pk = True
    column_searchable_list = (User.id, User.first_name, User.last_name, User.email, User.contact_no)


class SolutionModeView(ModelView):
    column_display_pk = True
    column_searchable_list = (Solution.id, Solution.lang_ext,
                              Solution.result_code, Solution.user_id,
                              Solution.problem_id)
    column_display_all_relations = True


class ProblemModeView(ModelView):
    column_display_pk = True
    column_searchable_list = (Problem.id, Problem.difficulty_level, Problem.category)
    create_template = 'admin/edit.html'
    edit_template = 'admin/edit.html'


admin.add_view(UserModelView(User, get_db_session()))
admin.add_view(ProblemModeView(Problem, get_db_session()))
admin.add_view(SolutionModeView(Solution, get_db_session()))
