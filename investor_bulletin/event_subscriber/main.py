import json
import pika
import pika.credentials
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from resources.alerts.alert_schema import AlertCreate
from resources.alerts import alert_service
from db.models import SessionLocal

# load from from .env
load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")
QUEUE_NAME = os.getenv("QUEUE_NAME")

BINDING_KEYS = ["alert.*"]  # listen for all alert events


def on_event(ch, method, properties, body):
    """Process incoming messages."""

    # get db session
    db_session = SessionLocal()
    try:
        data = json.loads(body.decode())
        alert = AlertCreate.model_validate(data)

        print(f"Received pydantic object: {alert}")

        # save alert to db
        alert_service.create_alert(alert, db_session)

        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Reject message


def on_close(connection, channel):
    """Handles shutdown signals (SIGINT, SIGTERM)."""
    print("\nShutting down gracefully...")

    if channel:
        channel.stop_consuming()
        print("Stopped consuming messages.")

    if connection:
        connection.close()
        print("Connection closed.")


def consume_message():
    """Consumes messages from RabbitMQ using Pika."""

    # set credentials
    credentials = pika.PlainCredentials(
        username=RABBITMQ_USER, password=RABBITMQ_PASSWORD
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the exchange (so it exists before binding)
    channel.exchange_declare(
        exchange=EXCHANGE_NAME, exchange_type="topic", durable=True
    )

    # Declare queue (only in consumer)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Bind queue to exchange with routing key pattern
    for binding_key in BINDING_KEYS:
        channel.queue_bind(
            exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=binding_key
        )

    print(f"Waiting for messages on '{QUEUE_NAME}' with keys {BINDING_KEYS}...")

    # Start consuming messages
    channel.basic_consume(
        queue=QUEUE_NAME, on_message_callback=on_event, auto_ack=False
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        on_close(connection, channel)


if __name__ == "__main__":

    consume_message()
