import os

from judge_temp import app
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads, TEXT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base,User

engine = create_engine(app.config['DB_URI'])
Base.metadata.bind=engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

profilePics = UploadSet('profilePics',extensions=IMAGES)
testcaseFiles = UploadSet('testcaseFiles',extensions=TEXT)
configure_uploads(app,profilePics)
configure_uploads(app,testcaseFiles)

def insertToDb(obj):
    """insertToDb(obj)-->True/False"""
    try:
        session.add(obj)
        session.commit()
        get
        return True
    except:
        return False

def saveProfilePic(pic,registrationNumber):
    """
        Saves profile pic of each user in /static/profile_pic_db/
        with their registrationNumber
    """
    profilePics.save(pic,name=str(registrationNumber)+"."+getExtensionOfFile(pic.filename))

def saveTestCases(filelist,id,typeOfFile):
    if typeOfFile==app.config['FILE_INPUT_TESTCASE']:
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

        Keyword arguments:
            filename -- name of the file

        getExtensionOfFile(filename) -> str
    """
    return filename.rsplit('.', 1)[1]
