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


def create_db_session():
    engine = create_engine(app.config['DB_URI'])
    Base.metadata.bind = engine

    db_session = sessionmaker(bind=engine)()

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


admin.add_view(UserModelView(User, create_db_session()))
admin.add_view(ProblemModeView(Problem, create_db_session()))
admin.add_view(SolutionModeView(Solution, create_db_session()))
