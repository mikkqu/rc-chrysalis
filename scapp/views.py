from flask import Flask, session, url_for, flash, redirect, request, render_template

from . import app
from . import models
from . import profiles


from .oauth import auth, get_login, login_required


def session_init(resp, next_url):
    session['oauth_token'] = (resp['access_token'], resp['refresh_token'])

    me = auth.get('people/me')
    if me.status is not 200:
        flash('Could not get the user info!')
        print('Unexpected status of oauth request: ' + str(me.status))
        return redirect(next_url)

    session["login"] = {}
    session["login"]["id"] = me.data["id"]
    session["login"]["name"] = me.data["first_name"] + " " + me.data["last_name"]
    session["login"]["avatar"] = me.data["image"]

    profiles.get_login_profile(me)


@app.route('/oauth_authorized')
def oauth_authorized():
    next_url = request.args.get('return_url') or url_for('profile')

    resp = auth.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(next_url)

    session_init(resp, next_url)

    return redirect(next_url)


@app.route('/login')
def login():
    if get_login():
        flash('You are already logged in.')
        return redirect(request.referrer or url_for('profile'))
    else:
        afterward = request.args.get('return_url') or request.referrer or None
        landing = url_for('oauth_authorized', return_url=afterward, _external=True)
        return auth.authorize(callback=landing)


@app.route('/logout')
def logout():
    session.pop('login', None)

    return redirect(url_for('index'))


@app.route("/")
def index():
    login = get_login()

    if login is not None:
        client = app.test_client()
        return client.get('/profile/', headers=list(request.headers))
    else:
        return render_template('index.html', profile=None)


@app.route('/profile/')
@login_required
def profile(login=None):
    uid=login["id"]

    profile = profiles.get_profile_by_uid(uid)
    if profile is None:
        return '<h1>Profile with id: %d has not been created!</h1>' % uid

    profile["score"] = 0
    profile["position"] = 0
    profile["level"] = ""

    return render_template('profile.html', login=login,
                                           profile=profile,
                                           goals=models.goals)
