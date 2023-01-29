import logging
import os

from flask import Flask, render_template
from flask_migrate import Migrate

from server.db import User, db
from server.login_manager import login_manager


def create_app(test_config=None):
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("server.default_settings")
    app.config.from_prefixed_env()

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    if is_gunicorn:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_logger.handlers)
    else:
        pass

    app.logger.setLevel(logging.INFO)

    if is_gunicorn:
        app.logger.info("Running in gunicorn")
    else:
        app.logger.info("Running in debug")

    app.logger.info("Database URI: " + app.config["SQLALCHEMY_DATABASE_URI"])

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

    app.logger.info("Finished initializing database")

    return app
