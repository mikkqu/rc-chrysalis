from flask import Flask, session, url_for, flash, redirect, request, render_template

from . import app

@app.route("/")
def index():
    return render_template('index.html', profile=None)
