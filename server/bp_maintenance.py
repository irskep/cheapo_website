from flask import Blueprint, render_template

bp = Blueprint("maintenance", "maintenance", url_prefix="")


@bp.route("/", methods=["GET"])
def index():
    return render_template("maintenance/index.html")


@bp.route("/_health", methods=["GET"])
def _health():
    # This route is used during deployment to check that the server process is running.
    return "OK"
