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

from .. import app
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, TEXT
from ..models import TestcaseFileType
from . import getExtensionOfFile
import os
import execution

# Intializing UploadSets
profilePics = UploadSet('profilePics',extensions=IMAGES)
testcaseFiles = UploadSet('testcaseFiles',extensions=TEXT)

# Configuring UploadSets
configure_uploads(app,profilePics)
configure_uploads(app,testcaseFiles)

def saveProfilePic(pic,registrationNumber):
    """
        Saves profile pic of each user in /static/profilePics/
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


def saveSourceCode(srcCode, codeLang, userId, problemId):
    """
        Saves soruce code submitted by each user. Each user gets a separate
        folder for storing solution. Folder structure that is used:
        /static/sourceCodeFiles/<regNo>/<problemId>/<srcFile>.<lang_ext>.
        For multiple uploads it'll get a suffix as a count.

        Args:
            srcCode (str) : contains text of solution code submitted by user.
            codeLang (str) : extension of file to be used. This extension will be
                as per the language chosen by user.
            userId (str) : registration number of user who uploaded this file
            problemId (int) : id of problem for which user submitted solution.
    """

    # TODO: apply check on success i.e. True if succes, False otherwise and raise an errors
    print 'inside saving'

    #Writing a single solution file
    userSolutionDirectory = os.path.join(app.config['SOURCE_CODE_FILES_DEST'],userId)
    srcCodeBuffer = open(os.path.join(userSolutionDirectory,'Solution.'+codeLang),"w")
    srcCodeBuffer.write(srcCode)
    srcCodeBuffer.close()

    # execution.start(userId, codeLang,problemId)
