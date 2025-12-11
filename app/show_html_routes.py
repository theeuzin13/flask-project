from flask import Blueprint, render_template, request, redirect
import uuid
from app.extensions import db
from flask_jwt_extended import jwt_required
from app.models import Show, Client, Place

html_show_bp = Blueprint("html_shows", __name__)

@html_show_bp.get("/shows")
@jwt_required()
def shows_page():
    shows = Show.query.all()
    clients = Client.query.all()
    places = Place.query.all()
    return render_template("shows_list.html",
                           shows=shows,
                           clients=clients,
                           places=places)

@html_show_bp.get("/shows/new")
@jwt_required()
def new_show_page():
    clients = Client.query.all()
    places = Place.query.all()
    return render_template("show_form.html", show=None, clients=clients, places=places)

@html_show_bp.post("/shows/new")
@jwt_required()
def create_show_html():
    data = request.form

    new_show = Show(
        uuid=str(uuid.uuid4()),
        show_date=data["show_date"],
        show_hour=data["show_hour"],
        value=data["value"],
        clients_uuid=data["client"],
        places_uuid=data["place"]
    )

    db.session.add(new_show)
    db.session.commit()

    return redirect("/shows")
