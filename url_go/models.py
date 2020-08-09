import string
from datetime import datetime
from random import choices

from .extensions import db 

class Url(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    full_url = db.Column(db.String(256))
    short_url = db.Column(db.String(8), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)
    creator_ip = db.Column(db.String(15), db.ForeignKey('users.ip'))
    creator = db.relationship("User")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_code()

    def generate_short_code(self):
        characters = string.digits + string.ascii_letters
        code = ''.join(choices(characters, k=8))

        dbresult = self.query.filter_by(short_url=code).first()

        if dbresult:
            return self.generate_short_link()
        
        return code
    
class User(db.Model):
    __tablename__ = "users"

    ip = db.Column(db.String(15), primary_key=True)
    urls_created = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
