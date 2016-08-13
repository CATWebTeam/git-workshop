from flask import Flask
from app import config

App = Flask(__name__)
App.config.from_object(config)
from app import views
