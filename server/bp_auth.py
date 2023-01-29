from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user
from server.db import User, db

bp = Blueprint("auth", "auth", url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."

        if error is None:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            error = "Incorrect username or password"

        next_url = url_for("inside.dashboard")

        if error is None:
            user = User.query.filter_by(email=email).first()
            login_user(user)
            return redirect(next_url)

        flash(error)
    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("outside.index"))
