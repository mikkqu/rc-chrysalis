from functools import wraps
from flask import session, request, redirect, url_for
from flask_oauthlib.client import OAuth, OAuthException

from . import app

auth = OAuth().remote_app(
    'recurse',
    base_url            = 'https://www.recurse.com/api/v1/',
    access_token_url    = 'https://www.recurse.com/oauth/token',
    authorize_url       = 'https://www.recurse.com/oauth/authorize',
    consumer_key        = app.config["CONSUMER_KEY"],
    consumer_secret     = app.config["CONSUMER_SECRET"],
    access_token_method = 'POST'
)


@auth.tokengetter
def get_token(token=None):
    # a decorated tokengetter function is required by the oauth module
    return session.get('oauth_token')


def get_login():
    # knowledge of session['login'] is only in here, oauth_authorized, and logout
    return session.get('login')


def login_required(route):
    # in large apps it is probably better to use the Flask-Login extension than
    # this route decorator because this decorator doesn't provide you with
    # 1. user access levels or
    # 2. the helpful abstraction of an "anonymous" user (not yet logged in)
    @wraps(route)
    def wrapper(*args, **kwargs):
        kwargs.update(login=get_login())

        if kwargs['login']:
            return route(*args, **kwargs)
        else:
            return redirect(url_for('login', return_url=request.url))
        # redirect includes "next=request.url" so that after logging in the
        # user will be sent to the page they were trying to access
    return wrapper