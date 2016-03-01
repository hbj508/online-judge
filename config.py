import os

#Address of the app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FOLDER_NAME = os.path.relpath(".","..")
APP_NAME = FOLDER_NAME

#database url
DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, APP_NAME,'db','judge_temp.db')

#flask uploads configuration
UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, APP_NAME, 'static')

#certain useful constatnts
FILE_INPUT_TESTCASE = 1
FILE_OUTPUT_TESTCASE = 2
