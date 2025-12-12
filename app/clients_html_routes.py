from flask import Blueprint, render_template, request, redirect, flash
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Client, Show
import uuid

html_clients_bp = Blueprint("html_clients", __name__)

@html_clients_bp.get("/clients")
@jwt_required()
def list_clients():
    search = request.args.get('search', '')
    query = Client.query
    
    if search:
        query = query.filter(
            (Client.name.ilike(f'%{search}%')) | 
            (Client.email.ilike(f'%{search}%'))
        )
    
    clients = query.all()
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

@html_clients_bp.get("/clients/<client_uuid>/edit")
@jwt_required()
def edit_client_page(client_uuid):
    client = Client.query.filter_by(uuid=client_uuid).first_or_404()
    return render_template("client_form.html", client=client)

@html_clients_bp.post("/clients/<client_uuid>/edit")
@jwt_required()
def edit_client(client_uuid):
    client = Client.query.filter_by(uuid=client_uuid).first_or_404()
    data = request.form
    client.name = data["name"]
    client.phone = data["phone"]
    client.email = data["email"]
    db.session.commit()
    return redirect("/clients")

@html_clients_bp.post("/clients/<client_uuid>/delete")
@jwt_required()
def delete_client(client_uuid):
    client = Client.query.filter_by(uuid=client_uuid).first_or_404()
    
    # Verificar se o cliente está vinculado a algum show
    show_linked = Show.query.filter_by(clients_uuid=client_uuid).first()
    
    if show_linked:
        flash("Não é possível apagar um cliente que está vinculado a um show!", "error")
        return redirect("/clients")
    
    db.session.delete(client)
    db.session.commit()
    return redirect("/clients")