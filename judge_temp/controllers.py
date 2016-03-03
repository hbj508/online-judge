import os

from judge_temp import app
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads, TEXT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,User, TestcaseFileType

"""
    This module acts as a controller i.e.creates interface between
    UI and backend.
"""

engine = create_engine(app.config['DB_URI'])
Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

profilePics = UploadSet('profilePics',extensions=IMAGES)
testcaseFiles = UploadSet('testcaseFiles',extensions=TEXT)
configure_uploads(app,profilePics)
configure_uploads(app,testcaseFiles)

def insertToDb(obj):
    """
        Inserts objects to database

        Args:
            obj: object to insert in database
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
            key: priamry key for particular object it's an optional parameter
        Returns:
            tuple(class): a tuple object if a key is provided
            list(tuple(class)): list of object in particular table
    """
    if key!=None:
        return session.query(ModelClass).filter_by(id=key).one()
    else:
        return session.query(ModelClass).all()


def saveProfilePic(pic,registrationNumber):
    """
        Saves profile pic of each user in /static/profilePics/
        with their registration number

        Args:
            pic(file): Picture file to be saved. It should not exceed 1MB
            registrationNumber(int): Registration number of student.
    """
    profilePics.save(pic,name=str(registrationNumber)+"."+getExtensionOfFile(pic.filename))

def saveTestCases(filelist,id,typeOfFile):
    """
        Saves input and output testcases by creating separate folder for each
        problem with their id in /static/testcaseFiles. Each file will be renamed
        to in<int>.txt and out<int>.txt. Uploaders are adviced to properly choose
        order for uploading files

        Args:
            filelist(list): list of input files, could be input or output testcases
            id(int): problem id
            typeOfFile(FileInput): enum of type FileInput which containts two values INPUT,OUTPUT
                        representing wether it's input testcase file or output.
    """
    if typeOfFile==TestcaseFileType.INPUT:
        foldername = str(id)+"/inputs"
        count = 1
        for testcaseFile in filelist:
            ext = getExtensionOfFile(testcaseFile.filename)
            filename = 'in' + str(count) + "." + ext
            testcaseFiles.save(testcaseFile,folder=foldername,name=filename)
            count += 1
    else:
        foldername = str(id)+"/outputs"
        count = 1
        for testcaseFile in filelist:
            ext = getExtensionOfFile(testcaseFile.filename)
            filename = 'out' + str(count) + "." + ext
            testcaseFiles.save(testcaseFile,folder=foldername,name=filename)
            count += 1

def getExtensionOfFile(filename):
    """
        Returns extension of a file in string format

        Args:
            filename(str): name of the file
        Returns:
            (str): extension of file
    """
    return filename.rsplit('.', 1)[1]
