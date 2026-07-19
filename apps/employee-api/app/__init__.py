import os

from flask import Flask

from app.extensions import db
from app.routes import api


def create_app(config=None):
    app = Flask(__name__)

    app.config["APP_NAME"] = "Employee API"
    app.config["VERSION"] = "1.0.0"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://employee_user:employee_password@localhost:5432/employee_db",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    app.register_blueprint(api)

    with app.app_context():
        from app import models

        db.create_all()

    return app
