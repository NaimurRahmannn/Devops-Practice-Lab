from flask import Flask

from app.routes import api


def create_app():
    app = Flask(__name__)

    app.config["APP_NAME"] = "Employee API"
    app.config["VERSION"] = "1.0.0"
    app.config["EMPLOYEES"] = []

    app.register_blueprint(api)

    return app
