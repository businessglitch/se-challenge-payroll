
from flask import Flask
from backend.blueprints.page import page
from backend.extensions import (db)

def create_app(settings_override=None):
    """[Create a Flask application using the app factory patter]
    :return: Flask app
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(page)
    extensions(app)
   
    return app

def extensions(app):
    """
    Register 0 or more extenstions (mutates the app thats passed in)

    :param app: Flask application instance
    :return: None
    """

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return None
