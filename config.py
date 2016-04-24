import os

SECRET_KEY = '[5\xac\xd4\xc7\xe6\xab\x87\xd03a\xff\x07\x01c\xdd\x1f\x00\xba\x12\xec\xba\xc42'

# Address of the app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FOLDER_NAME = os.path.relpath(".", "..")
APP_NAME = 'online_judge'

# database url
DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, APP_NAME, 'db', 'judge_temp.db')

# flask uploads configuration
UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, APP_NAME, 'static', 'rawFiles')
PROFILE_PICS_DEST = os.path.join(UPLOADS_DEFAULT_DEST,'profilePics')
SOLUTION_FILES_DEST = os.path.join(UPLOADS_DEFAULT_DEST, 'solutionFiles')
TEST_CASE_FILES_DEST = os.path.join(UPLOADS_DEFAULT_DEST, 'testCaseFiles')
