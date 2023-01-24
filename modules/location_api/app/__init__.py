import json
import logging, sys

from kafka import KafkaProducer

from flask import Flask, jsonify, request, g, Response
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    app.config.from_prefixed_env()
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    @app.before_request
    def before_request():
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        # Set up a Kafka producer
        TOPIC_NAME = app.config["KAFKA_TOPIC"]
        KAFKA_SERVER = app.config["KAFKA_SERVER"]
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        # Setting Kafka to g enables us to use this
        # in other parts of our application
        g.kafka_producer = producer

    return app

