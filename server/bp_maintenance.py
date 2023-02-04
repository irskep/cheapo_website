from flask import Blueprint, render_template

bp = Blueprint("maintenance", "maintenance", url_prefix="")


@bp.route("/", methods=["GET"])
def index():
    return render_template("maintenance/index.html")
