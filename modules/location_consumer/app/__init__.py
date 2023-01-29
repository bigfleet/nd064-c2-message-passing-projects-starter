import json
import os
import logging, sys

from flask import Flask, jsonify, request, g, Response
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(env=None):
    from app.config import config_by_name

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    # We'd have to upgrade Flash to get access to this-- I'm no pythonista
    #app.config.from_prefixed_env()

    DB_NAME = os.environ["DB_NAME"]
    api = Api(app, title="UdaConnect API", version="0.1.0")


    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app

