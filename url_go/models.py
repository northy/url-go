import string
from datetime import datetime
from random import choices

from .extensions import db, encode
from flask import current_app

class Url(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    full_url = db.Column(db.String(256))
    stats_id = db.Column(db.String(16))
    stats_secret = db.Column(db.String(256))
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)
    creator_ip = db.Column(db.String(15), db.ForeignKey('users.ip'))
    creator = db.relationship("User")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def generate_short_code(self):
        return encode(self.id,int(current_app.config['URL_OFFSET']),int(current_app.config['MINIMUM_URL_LENGTH']),current_app.config['URL_ALPHABET'])
    
class User(db.Model):
    __tablename__ = "users"

    ip = db.Column(db.String(15), primary_key=True)
    urls_created = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
