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
from sqlalchemy.orm import sessionmaker, relationship
from ..models import Base, User, Problem, Solution
from flask.ext.admin.contrib.sqla import ModelView

engine = create_engine(app.config['DB_URI'])
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autocommit=True)
db_session = DBSession()


class UserModelView(ModelView):
    column_display_pk = True
    column_searchable_list = ('id', 'first_name', 'last_name', 'email', 'contact_no')


class SolutionModeView(ModelView):
    column_display_all_relations = True
    column_display_pk = True


admin.add_view(UserModelView(User, db_session))
admin.add_view(ModelView(Problem, db_session))
admin.add_view(SolutionModeView(Solution, db_session))
