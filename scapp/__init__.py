# -*- coding: utf-8 -*-
"""
    rc_chrysalis
    ~~~~~

    A web service representing a casual social network to encourage
    social activities at Recurse Center.
"""

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='/static')

app.config.from_object('config')

mongo = PyMongo(app)

from . import views
