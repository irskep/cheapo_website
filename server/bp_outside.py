from flask import Blueprint, render_template

bp = Blueprint("outside", "outside", url_prefix="")


@bp.route("/", methods=["GET"])
def index():
    return render_template("outside/index.html")


@bp.route("/_health", methods=["GET"])
def _health():
    return "OK"
