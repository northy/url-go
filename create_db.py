from url_go import create_app
from url_go.extensions import db
from url_go.models import User, Url

print("Creating Database...")

app = create_app()

try:
    db.create_all(app=app)
except Exception as e :
    print("Error creating database:", e)
    exit(1)

print("Done!")
