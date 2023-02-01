import logging
import os
import subprocess
import sys

from flask import Flask, render_template, cli
from flask_migrate import Migrate

from server.db import User, db
from server.login_manager import login_manager


def create_app():
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("server.default_settings")
    app.config.from_prefixed_env()

    if is_gunicorn:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_logger.handlers)

    if os.environ.get("IS_SUBPROCESS"):
        app.logger.setLevel(logging.ERROR)
    else:
        app.logger.setLevel(logging.INFO)

    if is_gunicorn:
        app.logger.info("Running in gunicorn")
    else:
        app.logger.info("Running in debug")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate = Migrate(app, db)

    _maybe_run_migrations(app)

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

    app.logger.info("Database URI: " + app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        db.create_all()

    return app


def _maybe_run_migrations(app):
    """
    This function is only run in fly.io deploys. For Render deploys, you should use the normal
    Flask-Migrate process using the shell in the dashboard.

    This app uses a SQLite as its database. That's fine for performance, but it adds complexity to
    migrations, especially when deploying on fly.io, which uses LiteFS and requires that migrations
    happen in a subprocess of litefs.

    To get around that issue, this function does some really janky stuff
    1. See if Alembic (Flask-Migrate is a wrapper around Alembic) thinks we're in a good state
    2. If not, try to run migrations right away
    3. If that didn't work, it's possible you just naively ran db.create_all(), which doesn't
       set the Alembic version number. So just YOLO 'flask db stamp head' and hope the database
       isn't messed up.
    4. If the database still isn't in a good state, just fail the whole deploy because who knows
       what's going on.

    Notes:
    - We don't want to run this inside any regular command line stuff, otherwise we'll recursively
      spawn infinite subprocesses, so just bail out if 'db' is in the argument list
      (as in 'flask db migrate')
    - Also explicitly set an env var IS_SUBPROCESS=true so we never spawn more than one subprocesss

    If using Render instead of Fly.io, you could potentially delete all this and instead run your
    migrations manually in the shell. That would probably be the wiser thing to do.
    """
    if app.config.get("AUTOMIGRATE", False) != "true":
        app.logger.debug("(Skipping migration check because you didn't ask for it)")
        return
    if "db" in sys.argv:
        app.logger.info("(Skipping migration check inside CLI command)")
        return
    if os.environ.get("IS_SUBPROCESS"):
        app.logger.info("(Skipping migration check inside subprocess)")
        return
    app.logger.info(
        "Checking whether the database needs migrations applied by calling 'flask db check'..."
    )

    def run(args):
        my_env = os.environ.copy()
        my_env["IS_SUBPROCESS"] = "true"
        app.logger.info("> " + " ".join(args))
        return subprocess.run(args, env=my_env)

    result_check = run(["flask", "--app=server", "db", "check"])
    if result_check.returncode == 0:
        app.logger.info("Database looks OK; not running any migrations")
        return

    app.logger.warn("Looks like the database needs some work.")

    migrate_check = run(["flask", "--app=server", "db", "migrate"])
    if migrate_check.returncode == 0:
        app.logger.info(
            "The migration appears to have succeeded. Carrying on with creating the Flask app."
        )
        return
    else:
        app.logger.warn(
            "That didn't work. It's probably because the tables already exist. I'm just going to stamp this."
        )

    # The safest thing to do would be to destroy your database and start over, so feel free to
    # delete the following lines and just call sys.exit(1) instead.

    stamp_check = run(["flask", "--app=server", "db", "stamp", "head"])
    if stamp_check.returncode != 0:
        app.logger.error(
            "Couldn't stamp database with migration head. Sorry, your deploy can't continue."
        )
        sys.exit(1)
