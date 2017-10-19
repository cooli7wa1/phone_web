from datetime import timedelta
from flask import Flask, session
from werkzeug.utils import find_modules, import_string
from model import register_db

def create_app(config_filename):
    app = Flask(__name__)
    app.config.update(dict(
        DEBUG=False,
        DEVELOPMENT=False,
    ))
    app.config.from_pyfile(config_filename)
    register_blueprints(app)
    register_db(app)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)

    return app


def register_blueprints(app):
    for name in find_modules('app.views'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None

