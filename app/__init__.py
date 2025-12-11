from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .auth_routes import auth_bp
from .show_routes import show_bp
from .show_html_routes import html_show_bp
from .clients_html_routes import html_clients_bp
from .places_html_routes import html_places_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(html_show_bp)
    app.register_blueprint(html_clients_bp)
    app.register_blueprint(html_places_bp)
    app.register_blueprint(show_bp, url_prefix="/shows")

    return app
