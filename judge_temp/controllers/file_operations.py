"""
This module consists of all the file operations required for
online judge. Various tasks such as saving profile pics, saving user source code,
saving testcase files etc. It'll configure upload files using configure_uploads() available
in Flask-Uploads.

Attributes:
    profile_pics (UploadSet) : instance of UploadSet for saving profile pics.
        UploadSet is class available within Flask-Uploads package. It's responsible
        for saving different files.
    test_case_files (UploadSet) : instance of UploadSet for saving input and output testcases
        uploaded by problem setter.
"""

from .. import app, admin
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, TEXT
from flask.ext.admin.contrib.fileadmin import FileAdmin
from ..models import TestCaseFileType
from . import get_extension_of_file
import os
import execution

# static directory of files
static_dir_path = str(app.static_folder)

# Initializing UploadSets
profile_pics = UploadSet('profilePics', extensions=IMAGES)
test_case_files = UploadSet('testCaseFiles', extensions=TEXT)

# Configuring UploadSets
configure_uploads(app, profile_pics)
configure_uploads(app, test_case_files)

# adding admin views
raw_files_view = FileAdmin(os.path.join(static_dir_path, 'rawFiles'), name='Raw Files')
admin.add_view(raw_files_view)


def save_profile_pic(pic, reg_no):
    """
        Saves profile pic of each user in /static/rawFiles/profilePics/
        with their registration number

        Args:
            pic(file): Picture file to be saved. It should not exceed 1MB
            reg_no(str): Registration number of student.
    """
    # TODO: apply check on size of image
    profile_pics.save(pic, name=str(reg_no) + "." + get_extension_of_file(pic.filename))


def save_test_cases(file_list, problem_id, type_of_file):
    """
        Saves input and output testcases by creating separate folder for each
        problem with their problem_id in /static/rawFiles/testCaseFiles. Each file will be renamed
        to in<int>.txt and out<int>.txt. Uploaders are adviced to properly choose
        order for uploading files

        Args:
            file_list(list): list of input files, could be input or output testcases
            problem_id(int): problem problem_id
            type_of_file(FileInput): enum of type FileInput which containts two values INPUT,OUTPUT
                        representing wether it's input testcase file or output.
    """
    if type_of_file == TestCaseFileType.INPUT:
        folder_name = str(problem_id) + "/inputs"
        count = 1
        for testCaseFile in file_list:
            ext = get_extension_of_file(testCaseFile.filename)
            filename = 'in' + str(count) + "." + ext
            test_case_files.save(testCaseFile, folder=folder_name, name=filename)
            count += 1
    else:
        folder_name = str(problem_id) + "/outputs"
        count = 1
        for testCaseFile in file_list:
            ext = get_extension_of_file(testCaseFile.filename)
            filename = 'out' + str(count) + "." + ext
            test_case_files.save(testCaseFile, folder=folder_name, name=filename)
            count += 1
