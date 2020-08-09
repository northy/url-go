from url_go import create_app
from url_go.extensions import db
from url_go.models import User, Url

print("Creating Database...")

db.create_all(app=create_app())
