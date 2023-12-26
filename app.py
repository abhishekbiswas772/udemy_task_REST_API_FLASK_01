from flask import Flask
from db import db
from flask_smorest import Api
from dotenv import load_dotenv
import os
from resources.car import blp as CarBluePrint
from flask_migrate import Migrate



def create_app(DATABASE_URL = None):
    app = Flask(__name__)
    load_dotenv()
    app.config["API_VERSION"] = os.getenv("API_VERSION", "v1")
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = os.getenv("API_TITLE", "Cars-API")
    app.config["OPENAPI_VERSION"] = os.getenv("OPENAPI_VERSION", "3.0.3")
    app.config["OPENAPI_URL_PREFIX"] = os.getenv("OPENAPI_URL_PREFIX", "/")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = os.getenv("OPENAPI_SWAGGER_UI_PATH", "/swagger-ui")
    app.config["OPENAPI_SWAGGER_UI_URL"] = os.getenv("OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL or os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    api.register_blueprint(CarBluePrint)
    return app

