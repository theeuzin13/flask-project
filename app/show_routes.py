from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models import Show, Paid
import uuid
from datetime import datetime

show_bp = Blueprint("shows", __name__)


@show_bp.get("/")
@jwt_required()
def list_shows():
    query = Show.query

    date = request.args.get("date")
    client = request.args.get("client")

    if date:
        query = query.filter(Show.show_date == date)

    if client:
        query = query.filter(Show.clients_uuid == client)

    shows = query.all()

    return jsonify([
        {
            "uuid": s.uuid,
            "date": s.show_date.isoformat(),
            "hour": str(s.show_hour),
            "value": str(s.value),
            "paid": s.paid,
            "client": s.client.name,
            "place": s.place.name
        }
        for s in shows
    ])


@show_bp.post("/")
@jwt_required()
def create_show():
    data = request.json

    show = Show(
        uuid=str(uuid.uuid4()),
        show_date=data["show_date"],
        show_hour=data["show_hour"],
        value=data["value"],
        clients_uuid=data["client"],
        places_uuid=data["place"]
    )

    db.session.add(show)
    db.session.commit()

    return jsonify({"message": "Show created"}), 201


@show_bp.patch("/<id>")
@jwt_required()
def update_show(id):
    data = request.json
    show = Show.query.get_or_404(id)

    show.show_date = data.get("show_date", show.show_date)
    show.show_hour = data.get("show_hour", show.show_hour)
    show.value = data.get("value", show.value)

    db.session.commit()

    return jsonify({"message": "Updated"})


@show_bp.delete("/<id>")
@jwt_required()
def delete_show(id):
    show = Show.query.get_or_404(id)
    db.session.delete(show)
    db.session.commit()

    return jsonify({"message": "Deleted"})


@show_bp.post("/<id>/pay")
@jwt_required()
def mark_paid(id):
    show = Show.query.get_or_404(id)
    show.paid = True

    payment = Paid(
        uuid=str(uuid.uuid4()),
        show_uuid=id,
        paid_value=show.value
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify({"message": "Show marked as paid"})
