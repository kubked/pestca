from flask import Flask

from .views import api


def make_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app

