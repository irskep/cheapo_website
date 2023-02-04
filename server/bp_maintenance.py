from flask import Blueprint, render_template

bp = Blueprint("maintenance", "maintenance", url_prefix="")


@bp.route("/_health", methods=["GET"])
def _health():
    # This route is used during deployment to check that the server process is running.
    return "OK"


@bp.route("/", methods=["GET"], defaults={"path": ""})
@bp.route("/<path:path>", methods=["GET"])
def index(path):
    return render_template("maintenance/index.html")
