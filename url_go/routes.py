from flask import Blueprint, render_template, request, redirect, current_app, url_for, make_response

from .extensions import db, verify_hcaptcha, decode, check_url
from .models import Url, User

import json
from passlib.hash import sha256_crypt

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
    db.session.commit()
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
    if not full_url.startswith('http') : full_url = "http://"+full_url
    full_url,valid = check_url(full_url)
    
    if not valid :
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
    
    stats_id = request.form['stats_id']
    stats_secret = sha256_crypt.encrypt(request.form['stats_secret'])
    if stats_id == '' or request.form['stats_secret'] == '' : stats_id = None; stats_secret = None

    url = Url(full_url=full_url,creator_ip=ip,stats_id=stats_id,stats_secret=stats_secret)
    user.urls_created+=1
    db.session.add(url)
    db.session.commit()

    if stats_id is not None :
        resp = make_response(render_template('link_added.html', stats_id=stats_id, new_url=url.generate_short_code(), full_url=url.full_url))
        resp.set_cookie('stats_id', request.form['stats_id'])
        resp.set_cookie('stats_secret', request.form['stats_secret'])
        return resp

    return render_template('link_added.html', stats_id=stats_id, new_url=url.generate_short_code(), full_url=url.full_url)

@go.route('/stats')
def stats():
    ip=request.environ['REMOTE_ADDR']
    links = None
    if 'stats_id' in request.cookies.keys() and 'stats_secret' in request.cookies.keys() :
        links = Url.query.filter_by(stats_id=request.cookies.get('stats_id'))
        i=0
        links = links.all()
        while i<len(links) :
            if not sha256_crypt.verify(request.cookies.get('stats_secret'),links[i].stats_secret) : del links[i]
            else : i+=1
    
    return render_template('stats.html', links=links)

@go.route('/stats', methods=['POST'])
def stats_sendsecret():
    resp = make_response(redirect('stats'))
    resp.set_cookie('stats_id', request.form['stats_id'])
    resp.set_cookie('stats_secret', request.form['stats_secret'])

    return resp

@go.route('/delete', methods=['GET'])
def delete_url() :
    if not('stats_id' in request.cookies.keys() and 'stats_secret' in request.cookies.keys()) :
        return render_template('404.html'), 404
    
    url = Url.query.filter_by(id=request.args['id']).first_or_404()
    if request.cookies.get('stats_id')!=url.stats_id or not sha256_crypt.verify(request.cookies.get('stats_secret'),url.stats_secret) :
        return render_template('404.html'), 404
    
    db.session.delete(url)
    db.session.commit()

    return redirect('stats')

@go.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@go.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')
