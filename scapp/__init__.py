# -*- coding: utf-8 -*-
"""
    rc_chrysalis
    ~~~~~

    A web service representing a casual social network to encourage
    social activities at Recurse Center.
"""

from flask import Flask

app = Flask(__name__, static_url_path='/static')

app.config.from_object('config')

from . import views
