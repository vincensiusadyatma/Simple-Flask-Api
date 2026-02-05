from flask import Flask
from .config import Config

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app