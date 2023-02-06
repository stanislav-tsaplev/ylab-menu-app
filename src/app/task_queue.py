from os import getenv

from celery import Celery

from app.v1.processing import tasks  # noqa

BROKER_HOST = getenv("RABBITMQ_HOST", "localhost")
BROKER_PORT = getenv("RABBITMQ_PORT", 5672)
BROKER_USER = getenv("RABBITMQ_USER", "ylab")
BROKER_PASSWORD = getenv("RABBITMQ_PASSWORD", "ylab")


tq_engine = Celery(
    "celeryapp",
    broker=f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}//",
    backend="rpc://",
)
tq_engine.conf.task_routes = {"catalog.generate_xls_file": "celery"}
tq_engine.conf.update(task_track_started=True)
