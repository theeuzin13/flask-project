from .extensions import db
from datetime import datetime
from passlib.hash import bcrypt_sha256 as bcrypt

class User(db.Model):
    __tablename__ = "users"

    uuid = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    deleted_at = db.Column(db.DateTime)

    def set_password(self, pwd):
        self.password = bcrypt.hash(pwd)

    def check_password(self, pwd):
        return bcrypt.verify(pwd, self.password)


class Client(db.Model):
    __tablename__ = "clients"

    uuid = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(45))


class Place(db.Model):
    __tablename__ = "places"

    uuid = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(100))
    endereco = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cidade = db.Column(db.String(45))


class Show(db.Model):
    __tablename__ = "shows"

    uuid = db.Column(db.String(45), primary_key=True)
    show_date = db.Column(db.Date)
    show_hour = db.Column(db.Time)
    value = db.Column(db.Numeric(10,2))
    paid = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    places_uuid = db.Column(db.String(45), db.ForeignKey("places.uuid"))
    clients_uuid = db.Column(db.String(45), db.ForeignKey("clients.uuid"))

    place = db.relationship("Place")
    client = db.relationship("Client")


class Paid(db.Model):
    __tablename__ = "paids"

    uuid = db.Column(db.String(45), primary_key=True)
    show_uuid = db.Column(db.String(45), db.ForeignKey("shows.uuid"))
    date_paid = db.Column(db.DateTime, default=datetime.utcnow)
    paid_value = db.Column(db.Numeric(10, 2))

    show = db.relationship("Show")
