from flask_sqlalchemy import SQLAlchemy 

import requests

def verify_hcaptcha(secret,response,remoteip) :
    params = {'secret':secret,'response':response,'remoteip':remoteip}
    r = requests.post("https://hcaptcha.com/siteverify",params=params)
    return r.json()['success']

print("Starting database...")

db = SQLAlchemy()
