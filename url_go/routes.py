from flask import Blueprint, render_template, request, redirect, current_app, url_for

from .extensions import db, verify_hcaptcha, decode
from .models import Url, User

import validators
import json

go = Blueprint('go', __name__)

@go.route('/')
def index():
    if current_app.config['LIMIT_SHORTENS'] :
        ip=request.environ['REMOTE_ADDR']
        user = User.query.filter_by(ip=ip).first()
        if not user :
            user = User(ip=ip)
            db.session.add(user)
            db.session.flush()
        remaining = int(current_app.config['LIMIT_COUNT'])-user.urls_created
    else :
        remaining = 0
    return render_template('index.html', limited=current_app.config['LIMIT_SHORTENS'], remaining=remaining)

@go.route('/<short_url>')
def redirect_to_url(short_url):
    link = Url.query.filter_by(id=decode(short_url,int(current_app.config['URL_OFFSET']),current_app.config['URL_ALPHABET'])).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.full_url)

@go.route('/refresh', methods=['GET'])
def refresh() :
    ip=request.environ['REMOTE_ADDR']
    if ip!="127.0.0.1" : return render_template('404.html'), 404
    User.query.filter(User.urls_created>0).update({'urls_created': User.urls_created - 1})
    db.session.commit()

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@go.route('/new', methods=['POST'])
def new():
    if current_app.config['HCAPTCHA_ENABLED'] and not verify_hcaptcha(current_app.config['HCAPTCHA_SECRET_KEY'],request.form['h-captcha-response'],request.environ['REMOTE_ADDR']) :
        return render_template('error.html',error="Captcha could not be verified"), 400
    full_url = request.form['full_url']
    if not validators.url(full_url) :
        return render_template('error.html',error="Invalid URL"), 400
    
    ip=request.environ['REMOTE_ADDR']
    print(ip,"Shortened an URL!")

    user = User.query.filter_by(ip=ip).first()
    if not user :
        user = User(ip=ip)
        db.session.add(user)
        db.session.flush()
    
    if current_app.config['LIMIT_SHORTENS'] and user.urls_created>=int(current_app.config['LIMIT_COUNT']) :
        return render_template('error.html',error="You have exceeded your shortens limit"), 400
    
    url = Url(full_url=full_url,creator_ip=ip)
    user.urls_created+=1
    db.session.add(url)
    db.session.commit()
        
    return render_template('link_added.html', new_url=url.generate_short_code(), full_url=url.full_url)

@go.route('/stats')
def stats():
    ip=request.environ['REMOTE_ADDR']
    links = Url.query.filter_by(creator_ip=ip)

    return render_template('stats.html', links=links)

@go.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
