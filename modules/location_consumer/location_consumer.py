from app.udaconnect.schemas import LocationSchema
from app.udaconnect.models import Location
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base
                                                                                                                                                
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

import location_pb2
import location_pb2_grpc 

from kafka import KafkaConsumer, KafkaProducer
import os
import json
from concurrent.futures import ThreadPoolExecutor

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

TOPIC_NAME = os.environ["FLASK_KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["FLASK_KAFKA_SERVER"]



consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER
)

def locationProcess(data):
  print(data)
  
  new_location = Location()
  new_location.person_id = location["person_id"]
  new_location.creation_time = location["creation_time"]
  new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
    
  db.session.add(new_location)
  db.session.commit()


for inf in consumer:
  inf_data = inf.value
  locationProcess(inf_data)