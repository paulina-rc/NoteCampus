from flask import Blueprint, render_template, request, redirect, url_for

from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for("auth.dashboard"))

    return render_template("login.html")

@auth.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")