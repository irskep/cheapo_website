from flask import Blueprint, render_template, g, redirect, url_for, current_app
from flask_login import current_user

bp = Blueprint("outside", "outside", url_prefix="")


@bp.route("/", methods=["GET"])
def index():
    if not current_user.is_anonymous:
        return redirect(url_for("inside.dashboard"))
    return render_template("outside/index.html")


@bp.route("/_health", methods=["GET"])
def _health():
    # This route is used during deployment to check that the server process is running.
    return "OK"
