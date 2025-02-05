""" Alert DAL"""

"""_summary_
this file is to right any ORM logic for the Alert model
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models import Alert
from resources.alerts.alert_schema import AlertCreate


def create_alert(alert: AlertCreate, session: Session) -> Alert:
    try:
        db_alert = Alert(**alert.model_dump())  # schema to model converison
        session.add(db_alert)
        session.commit()
        session.refresh(db_alert)
        return db_alert
    except SQLAlchemyError as e:
        print(f"Database error in create_alert: {e}")
        session.rollback()
        return None


def get_alerts(offset: int, limit: int, session: Session) -> list[Alert]:
    try:
        return session.query(Alert).offset(offset).limit(limit).all()
    except SQLAlchemyError as e:
        print(f"Database error in get_alerts: {e}")
        session.rollback()
        return []
