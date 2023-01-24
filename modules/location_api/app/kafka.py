import click

from flask import current_app, g

from kafka import KafkaProducer

def get_producer():
    if 'producer' not in g:
        g.producer = KafkaProducer(bootstrap_servers=current_app.config['KAFKA_SERVER'])
        g.topic    = current_app.config['KAFKA_TOPIC']

    return g.producer


def close_producer(e=None):
    producer = g.pop('producer', None)
    if producer is not None:
        producer.close()

@click.command('kafka')
def init_producer():
    producer = get_producer()

def init_app(app):
    app.teardown_appcontext(close_producer)
    app.cli.add_command(init_producer)