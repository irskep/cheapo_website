import logging
import os

from flask import Flask, g
from flask_migrate import Migrate

from server.db import User, db
from server.login_manager import login_manager


def create_app():
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("server.default_settings")
    app.config.from_prefixed_env()

    is_maintenance = app.config.get("MAINTENANCE_MODE", False)

    if is_gunicorn:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_logger.handlers)

    if os.environ.get("IS_SUBPROCESS"):
        app.logger.setLevel(logging.ERROR)
    else:
        app.logger.setLevel(logging.INFO)

    if is_maintenance:
        app.logger.info("Running in maintenance mode")
        # load sqlalchemy read-only.
        app.config["SQLALCHEMY_DATABASE_URI"] += "?mode=ro"

        # if your app supports read-only database connections in general, for example if
        # almost all routes are for reads, then you could remove the special maintenance
        # blueprint and just serve your normal routes.
        from . import bp_maintenance

        app.register_blueprint(bp_maintenance.bp)

        # Initialize database stuff so we can run migrations on the command line
        db.init_app(app)
        Migrate(app, db)

        return app

    if is_gunicorn:
        app.logger.info("Running in gunicorn")
    else:
        app.logger.info("Running in the Flask debug server")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        g.current_user = user
        return user

    ### blueprints ###

    from . import bp_auth, bp_inside, bp_outside

    app.register_blueprint(bp_auth.bp)
    app.register_blueprint(bp_inside.bp)
    app.register_blueprint(bp_outside.bp)

    ### commands ###

    app.logger.info("Database URI: " + app.config["SQLALCHEMY_DATABASE_URI"])

    return app
