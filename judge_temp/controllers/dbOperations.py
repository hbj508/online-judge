"""
This module is used for performing all database operations
required for the applications. It creates engine required for
db operations and also intializes sessionmaker for creating a sesssion to
make transations.

Attributes:
    engine (Engine): instance of .Engine class of sqlalchemy to work with database
    DBSession (Session): .Session class from sqlalchemy module wtih given configuration.
        Currently it only intializes it with bind=engine
    sesssion (DBSession):  instance of DBSession() to perform transations with database
"""

from .. import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import Base


engine = create_engine(app.config['DB_URI'])
Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def insertToDb(obj):
    """
        Inserts objects to database

        Args:
            obj: object to insert in database

        Returns:
            bool: True if successful, False otherwise.
    """
    try:
        session.add(obj)
        session.commit()
        return True
    except:
        return False


def selectFromDb(ModelClass,key=None):
    """
        Selects a particular row from a table based on its key if a key is provided
        otherwise returns list of all tuples of given class

        Args:
            ModelClass: model class to query i.e. which table you want to extract from
            key (Optional): priamry key for particular object it's an optional parameter.
                If provided it'll return particular row info otherwise list of rows of ModelClass
                used.
        Returns:
            tuple(class): a tuple object if a key is provided
            (list(tuple(ModelClass))): list of object in particular table

        Note: ModelClass is just class used to define table in models
    """
    if key!=None:
        return session.query(ModelClass).filter_by(id=key).one()
    else:
        return session.query(ModelClass).all()
