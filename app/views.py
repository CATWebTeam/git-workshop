from flask import Flask
from flask import render_template
from app import App
from app import utils
from app import config

@App.route('/')
def public_timeline():
    return render_template('html_puplic.html',flashes = utils.get_all_twittes())
