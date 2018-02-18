from flask import Flask

from pestca.api import api
from pestca.error_handlers import ErrorHandler


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    register_errorhandlers(app)
    return app


def register_errorhandlers(app):
    app.errorhandler(ErrorHandler)(lambda e: e.to_json())
