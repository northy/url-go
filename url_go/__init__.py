from flask import Flask

from .extensions import db
from .routes import go

def create_app(config_file='settings.py'):
    global hcaptcha

    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    print("Starting database...")

    db.init_app(app)

    app.register_blueprint(go)

    if (app.config['HCAPTCHA_ENABLED']) :
        print("Enabling hCaptcha...")

    return app
