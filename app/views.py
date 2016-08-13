from flask import Flask
from flask import render_template

from app import App
from app import db_utils
from app import config

@App.route('/')
def public_timeline():
    return render_template('public_timeline.html', flashes=db_utils.get_all_twittes())

@app.route('/<name>')
def private_timeline(name):
    return render_template('public_timeline.html', flashes=db_utils.get_user_timeline_twittes(name))
