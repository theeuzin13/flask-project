from flask import Blueprint, render_template, request, redirect
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import uuid

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/login")
def login_page():
    return render_template("login.html")


@auth_bp.post("/login")
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return render_template("login.html", error="Credenciais inválidas")

    token = create_access_token(identity=user.uuid)
    resp = redirect("/shows")
    set_access_cookies(resp, token)

    return resp


@auth_bp.get("/register")
def register_page():
    return render_template("register.html")


@auth_bp.post("/register")
def register():
    data = request.form

    user = User(
        uuid=str(uuid.uuid4()),
        name=data["name"],
        email=data["email"]
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return redirect("/login")


@auth_bp.get("/logout")
def logout():
    resp = redirect("/login")
    unset_jwt_cookies(resp)
    return resp
