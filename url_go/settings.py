import string

SERVER_NAME = "127.0.0.1:5001"
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

HCAPTCHA_ENABLED = False
HCAPTCHA_SITE_KEY = ''
HCAPTCHA_SECRET_KEY = ''

LIMIT_SHORTENS = False
LIMIT_COUNT = 0

MINIMUM_URL_LENGTH = 4
URL_OFFSET = 0
URL_ALPHABET = string.ascii_letters + string.digits