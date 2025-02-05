from email import message
import amqpstorm
import json
from dotenv import load_dotenv
import os
from resources.alerts.alert_schema import AlertCreate

# load from from .env
load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")


def publish_message(routing_key: str, message: AlertCreate):

    try:
        # connect to rabbitmq
        connection = amqpstorm.Connection(
            hostname=RABBITMQ_HOST, username=RABBITMQ_USER, password=RABBITMQ_PASSWORD
        )
        channel = connection.channel()

        # declare exchange
        channel.exchange.declare(
            exchange=EXCHANGE_NAME, exchange_type="topic", durable=True
        )

        # message to json
        message_body = json.dumps(message.model_dump())

        # Publish message
        channel.basic.publish(
            body=message_body, exchange=EXCHANGE_NAME, routing_key=routing_key
        )

        print(f"Published message: {message} with routing_key: {routing_key}")

        # Close connection
        connection.close()
    except amqpstorm.AMQPError as e:
        print(f"Error publishing message: {e}")


if __name__ == "__main__":

    message = AlertCreate(symbol="AAPL", trigger_price=100, threshold_price=95)

    publish_message(routing_key="alert.created", message=message)
