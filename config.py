import os

#Address of the app
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FOLDER_NAME = os.path.relpath(".","..")
APP_NAME = 'judge_temp'

#database url
DB_URI = 'sqlite:///' + os.path.join(BASE_DIR, APP_NAME,'db','judge_temp.db')

#flask uploads configuration
UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, APP_NAME, 'static')
SOURCE_CODE_FILES_DEST = os.path.join(UPLOADS_DEFAULT_DEST,'sourceCodeFiles')
