from flask import Blueprint, render_template, request, redirect
import uuid
from app.extensions import db
from flask_jwt_extended import jwt_required
from app.models import Show, Client, Place, Paid

html_show_bp = Blueprint("html_shows", __name__)

@html_show_bp.get("/shows")
@jwt_required()
def shows_page():
    search = request.args.get('search', '')
    query = Show.query
    
    if search:
        query = query.join(Client, Show.clients_uuid == Client.uuid, isouter=True).join(Place, Show.places_uuid == Place.uuid, isouter=True).filter(
            (Client.name.ilike(f'%{search}%')) | 
            (Place.name.ilike(f'%{search}%'))
        ).distinct()
    
    shows = query.all()
    clients = Client.query.all()
    places = Place.query.all()
    return render_template("shows_list.html",
                           shows=shows,
                           clients=clients,
                           places=places)

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

@html_show_bp.get("/shows/new")
@jwt_required()
def new_show_page():
    clients = Client.query.all()
    places = Place.query.all()
    return render_template("show_form.html", show=None, clients=clients, places=places)

@html_show_bp.get("/shows/<id>/edit")
@jwt_required()
def edit_show_page(id):
    show = Show.query.get_or_404(id)
    clients = Client.query.all()
    places = Place.query.all()
    return render_template("show_form.html", show=show, clients=clients, places=places)


@html_show_bp.post("/shows/<id>/edit")
@jwt_required()
def update_show_html(id):
    show = Show.query.get_or_404(id)
    data = request.form

    show.show_date = data["show_date"]
    show.show_hour = data["show_hour"]
    show.value = data["value"]
    show.clients_uuid = data["client"]
    show.places_uuid = data["place"]

    db.session.commit()
    return redirect("/shows")

@html_show_bp.post("/shows/<id>/delete")
def delete_show_html(id):
    Paid.query.filter_by(show_uuid=id).delete()

    show = Show.query.get_or_404(id)
    db.session.delete(show)
    db.session.commit()

    return redirect("/shows")



