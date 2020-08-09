import os 

SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
try :
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
except : pass
SQLALCHEMY_TRACK_MODIFICATIONS = False

HCAPTCHA_ENABLED = False
HCAPTCHA_SITE_KEY = ''
HCAPTCHA_SECRET_KEY = ''

try:
    HCAPTCHA_ENABLED = os.environ.get('HCAPTCHA_ENABLED')
    HCAPTCHA_SITE_KEY = os.environ.get('HCAPTCHA_SITE_KEY')
    HCAPTCHA_SECRET_KEY = os.environ.get('HCAPTCHA_SECRET_KEY')
except: pass

LIMIT_SHORTENS = False
LIMIT_COUNT = 0
try:
    LIMIT_SHORTENS = os.environ.get('LIMIT_SHORTENS')
    LIMIT_COUNT = os.environ.get('LIMIT_COUNT')
except: pass

SERVER_NAME="127.0.0.1:5001"
try :
    SERVER_NAME=os.environ.get('SERVER_NAME')
except: pass

if (HCAPTCHA_ENABLED) :
    print("Enabling hCaptcha...")
