import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab
from resources.market import market_service
from resources.alert_rules import alert_rule_service as rule_service
from resources.alerts import alert_service
from core.messaging import publish_message
from db.models import SessionLocal

# load environment variables
load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}//"

# Connect Celery to RabbitMQ
app = Celery("tasks", broker=BROKER_URL, backend="rpc://")


@app.task
def check_alerts():
    print("\n---running check alerts---\n")
    # get db session
    db_session = SessionLocal()
    try:

        # fetch stocks data
        tickers_data = market_service.get_market_data()

        # get all alert rules
        rules = rule_service.get_all_alert_rules(db_session)

        # check if any stock passes given alert rules
        alerts = alert_service.check_alerts(tickers_data, rules)

        # publish alerts
        for alert in alerts:
            publish_message(routing_key="alert.created", message=alert)

        print(f"published {len(alerts)} alerts")
    except Exception as e:
        print(f"exception happened: {e}")
    finally:
        db_session.close()

    print("\n---finished check alerts---\n")


app.conf.beat_schedule = {
    "run-every-five-minutes": {
        "task": "tasks.check_alerts",
        "schedule": crontab(minute="*/5"),  # Runs every 5 mins
    },
}
