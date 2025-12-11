from flask import Blueprint, render_template, request, redirect
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Client
import uuid

html_clients_bp = Blueprint("html_clients", __name__)

@html_clients_bp.get("/clients")
@jwt_required()
def list_clients():
    clients = Client.query.all()
    return render_template("clients_list.html", clients=clients)

@html_clients_bp.get("/clients/new")
@jwt_required()
def new_client_page():
    return render_template("client_form.html")

@html_clients_bp.post("/clients/new")
@jwt_required()
def create_client():
    data = request.form
    client = Client(
        uuid=str(uuid.uuid4()),
        name=data["name"],
        phone=data["phone"],
        email=data["email"]
    )
    db.session.add(client)
    db.session.commit()
    return redirect("/clients")
