import pathlib

APPLICATION_ROOT = '/'
PARENT_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = PARENT_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
DATABASE_FILENAME = PARENT_ROOT/'var'/'voter_dex.sqlite3'

