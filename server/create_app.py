import logging
import os

from flask import Flask, render_template
from flask_migrate import Migrate

from server.db import User, db
from server.login_manager import login_manager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        LOG_WITH_GUNICORN=False,
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///project.db",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    if app.config["LOG_WITH_GUNICORN"]:
        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.INFO)
    else:
        pass

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    ### blueprints ###

    from . import bp_auth, bp_inside, bp_outside

    app.register_blueprint(bp_auth.bp)
    app.register_blueprint(bp_inside.bp)
    app.register_blueprint(bp_outside.bp)

    ### commands ###

    @app.cli.command("initdb")
    def initdb():
        db.create_all()

    with app.app_context():
        db.create_all()

    return app
