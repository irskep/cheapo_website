from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("inside", "inside", url_prefix="")


@bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("inside/dashboard.html")
