import os

from threading import Event
import signal

from flask_kafka import FlaskKafka

INTERRUPT_EVENT = Event()

bus = FlaskKafka(INTERRUPT_EVENT,
                 bootstrap_servers=",".join(os.environ("FLASK_KAFKA_SERVER")),
                 )

from app import create_app

def listen_kill_server():
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)


@bus.handle(os.environ("FLASK_KAFKA_TOPIC"))
def test_location_handler(msg):
    print("consumed {} from location".format(msg))

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    bus.run()
    listen_kill_server()
    app.run(debug=True)
