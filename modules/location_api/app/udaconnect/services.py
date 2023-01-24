import json

import logging
from datetime import datetime, timedelta
from typing import Dict, List

from flask import g
from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-api")

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        logging.debug("location: %r", location)
        # Turn order_data into a binary string for Kafka
        kafka_data = json.dumps(location).encode()
        # Kafka producer has already been set up in Flask context
        logging.debug("data: %r", kafka_data)
        g.producer.send(g.topic, kafka_data)
        
        # db.session.add(new_location)
        # db.session.commit()

        return location
