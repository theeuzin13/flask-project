from flask import Blueprint, request, jsonify, render_template, redirect
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import User
import uuid

user_bp = Blueprint("users", __name__)


@user_bp.get("/")
@jwt_required()
def list_users():
    query = User.query
    users = query.all()

    return jsonify([
        {
            "uuid": u.uuid,
            "name": u.name,
            "email": u.email,
            "created_at": u.created_at.isoformat()
        }
        for u in users
    ])

@user_bp.get("/list")
@jwt_required()
def list_users_page():
    search = request.args.get('search', '')
    query = User.query
    
    if search:
        query = query.filter(
            (User.name.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%'))
        )
    
    users = query.all()
    return render_template("users_list.html", users=users)

@user_bp.get("/new")
@jwt_required()
def new_user_page():
    return render_template("user_form.html")


@user_bp.post("/")
@jwt_required()
def create_user():
    data = request.json

    user = User(
        uuid=str(uuid.uuid4()),
        name=data["name"],
        email=data["email"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@user_bp.get("/<uuid>/edit")
@jwt_required()
def edit_user_page(uuid):
    user = User.query.get_or_404(uuid)
    return render_template("user_form.html", user=user)


@user_bp.post("/<uuid>/edit")
@jwt_required()
def update_user(uuid):
    user = User.query.get_or_404(uuid)
    
    user.name = request.form.get("name", user.name)
    user.email = request.form.get("email", user.email)

    db.session.commit()

    return redirect("/users/list")


@user_bp.post("/<uuid>/delete")
@jwt_required()
def delete_user(uuid):
    user = User.query.get_or_404(uuid)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users/list")


@user_bp.patch("/<uuid>/edit")
@jwt_required()
def update_user_api(uuid):
    data = request.json
    user = User.query.get_or_404(uuid)

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)

    db.session.commit()

    return jsonify({"message": "Updated"})


@user_bp.delete("/<uuid>/delete")
@jwt_required()
def delete_user_api(uuid):
    user = User.query.get_or_404(uuid)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Deleted"})