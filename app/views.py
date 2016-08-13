from flask import Flask
from flask import render_template

from app import App
from app import db_utils
from app import config

@App.route('/')
def public_timeline():
    twittes = db_utils.get_all_twittes()
    return render_template('public_timeline.html', twittes = twittes)

@App.route('/<name>')
def private_timeline(name):
    twittes =db_utils.get_user_timeline_twittes(name)
    return render_template('public_timeline.html', twittes = twittes )
