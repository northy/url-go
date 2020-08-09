from flask import Flask

from .extensions import db
from .routes import go

def create_app(config_file='settings.py'):
    global hcaptcha

    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    db.init_app(app)

    app.register_blueprint(go)

    return app
