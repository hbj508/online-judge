"""
This module consists of all the file operations required for
online judge. Various tasks such as saving profile pics, saving user source code,
saving testcase files etc. It'll configure upload files using configure_uploads() available
in Flask-Uploads.

Attributes:
    profilePics (UploadSet) : instance of UploadSet for saving profile pics.
        UploadSet is class available within Flask-Uploads package. It's responsible
        for saving different files.
    testcaseFiles (UploadSet) : instance of UploadSet for saving input and output testcases
        uploaded by problem setter.
"""

from .. import app, admin
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, TEXT
from flask.ext.admin.contrib.fileadmin import FileAdmin
from ..models import TestcaseFileType
from . import getExtensionOfFile
import os
import execution

#static directory of files
static_dir_path = str(app.static_folder)

# Intializing UploadSets
profilePics = UploadSet('profilePics',extensions=IMAGES)
testcaseFiles = UploadSet('testcaseFiles',extensions=TEXT)

# Configuring UploadSets
configure_uploads(app,profilePics)
configure_uploads(app,testcaseFiles)

#adding admin views
rawFilesView = FileAdmin(static_dir_path+'/rawFiles/',name='Raw Files')
admin.add_view(rawFilesView)

def saveProfilePic(pic,registrationNumber):
    """
        Saves profile pic of each user in /static/rawFiles/profilePics/
        with their registration number

        Args:
            pic(file): Picture file to be saved. It should not exceed 1MB
            registrationNumber(int): Registration number of student.
    """
    # TODO: apply check on size of image
    profilePics.save(pic,name=str(registrationNumber)+"."+getExtensionOfFile(pic.filename))

def saveTestCases(filelist,id,typeOfFile):
    """
        Saves input and output testcases by creating separate folder for each
        problem with their id in /static/rawFiles/testcaseFiles. Each file will be renamed
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
