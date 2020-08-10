from flask_sqlalchemy import SQLAlchemy 

import requests

def verify_hcaptcha(secret,response,remoteip) :
    params = {'secret':secret,'response':response,'remoteip':remoteip}
    r = requests.post("https://hcaptcha.com/siteverify",params=params)
    return r.json()['success']

def check_url(url) :
    prepared_request = requests.models.PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return prepared_request.url,True
    except :
        return '',False

def encode(numeric_id, offset, minimumLength, urlAlphabet) :
    base = len(urlAlphabet)
    numeric_id+=offset

    encoded = ""
    while (numeric_id//base>0) :
        encoded = urlAlphabet[numeric_id%base] + encoded
        numeric_id = numeric_id//base
    encoded = urlAlphabet[numeric_id%base] + encoded
    
    if len(encoded)<minimumLength :
        encoded = urlAlphabet[0]*(minimumLength-len(encoded))+encoded
    
    return encoded

def decode(encoded, offset, urlAlphabet) :
    base = len(urlAlphabet)
    
    multiplier = 1
    numeric_id = 0
    for x in encoded[::-1] :
        numeric_id+=multiplier*urlAlphabet.find(x)
        multiplier*=base
    numeric_id-=offset
    
    return numeric_id

db = SQLAlchemy()
