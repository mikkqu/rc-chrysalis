# -*- coding: utf-8 -*-
"""
    rc_chrysalis
    ~~~~~

    A web service representing a casual social network to encourage
    social activities at Recurse Center.
"""

import os
from flask import Flask
from flask_pymongo import PyMongo
from . import moment

app = Flask(__name__, static_url_path='/static')
app.jinja_env.globals['momentjs'] = moment.momentjs
app.jinja_env.auto_reload = True

heroku = os.getenv('IS_HEROKU', None)
if heroku is None:
    app.config.from_object('config')
else:
    app.config["MONGO_URI"] = os.environ['MONGO_URI']
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["CONSUMER_KEY"] = os.environ["CONSUMER_KEY"]
    app.config["CONSUMER_SECRET"] = os.environ["CONSUMER_SECRET"]

mongo = PyMongo(app)

from . import views
