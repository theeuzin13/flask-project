from flask import Blueprint, render_template, request, redirect
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Place
import uuid

html_places_bp = Blueprint("html_places", __name__)

@html_places_bp.get("/places")
@jwt_required()
def list_places():
    places = Place.query.all()
    return render_template("places_list.html", places=places)

@html_places_bp.get("/places/new")
@jwt_required()
def new_place_page():
    return render_template("place_form.html")

@html_places_bp.post("/places/new")
@jwt_required()
def create_place():
    data = request.form
    place = Place(
        uuid=str(uuid.uuid4()),
        name=data["name"],
        endereco=data["endereco"],
        estado=data["estado"],
        cidade=data["cidade"]
    )
    db.session.add(place)
    db.session.commit()
    return redirect("/places")

@html_places_bp.get("/places/<place_uuid>/edit")
@jwt_required()
def edit_place_page(place_uuid):
    place = Place.query.filter_by(uuid=place_uuid).first_or_404()
    return render_template("place_form.html", place=place)

@html_places_bp.post("/places/<place_uuid>/edit")
@jwt_required()
def edit_place(place_uuid):
    place = Place.query.filter_by(uuid=place_uuid).first_or_404()
    data = request.form
    place.name = data["name"]
    place.endereco = data["endereco"]
    place.estado = data["estado"]
    place.cidade = data["cidade"]
    db.session.commit()
    return redirect("/places")

@html_places_bp.post("/places/<place_uuid>/delete")
@jwt_required()
def delete_place(place_uuid):
    place = Place.query.filter_by(uuid=place_uuid).first_or_404()
    db.session.delete(place)
    db.session.commit()
    return redirect("/places")
