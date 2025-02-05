""" Alert Rule  DAL"""

"""_summary_
this file is to right any ORM logic for the Alert Rule model
"""
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from resources.alert_rules.alert_rule_schema import (
    AlertRuleBase,
    AlertRuleCreate,
    AlertRuleUpdate,
)

from db.models import AlertRule


def create_alert_rule(rule: AlertRuleCreate, session: Session) -> AlertRule:
    try:
        db_rule = AlertRule(
            **rule.model_dump()
        )  # schema(pydantic) to model(SQLAlchemy)
        session.add(db_rule)
        session.commit()
        session.refresh(db_rule)
        return db_rule
    except SQLAlchemyError as e:
        print(f"Database error in create_alert_rule: {e}")
        session.rollback()
        return None


def get_alert_rule(rule_id: UUID, session: Session) -> AlertRule:
    try:
        db_rule = session.get(AlertRule, rule_id)
        return db_rule
    except SQLAlchemyError as e:
        print(f"Database error in get_alert_rule: {e}")
        return None


def get_alert_rules(offset: int, limit: int, session: Session) -> list[AlertRule]:
    try:
        return session.query(AlertRule).offset(offset=offset).limit(limit=limit).all()
    except SQLAlchemyError as e:
        print(f"Database error in get_alert_rules: {e}")
        return []


def update_alert_rule(
    rule_id: UUID, rule_schema: AlertRuleUpdate, session: Session
) -> AlertRule:

    try:
        db_rule = session.get(AlertRule, rule_id)

        if not db_rule:
            return None

        # update changed fields
        for key, value in rule_schema.model_dump(exclude_unset=True).items():
            setattr(db_rule, key, value)

        session.commit()
        session.refresh(db_rule)
        return db_rule
    except SQLAlchemyError as e:
        print(f"Database error in update_alert_rule: {e}")
        session.rollback()
        return None


def delete_alert_rule(rule_id: UUID, session: Session) -> AlertRule:

    try:
        db_rule = session.get(AlertRule, rule_id)

        if not db_rule:
            return None

        session.delete(db_rule)
        session.commit()

        return db_rule
    except SQLAlchemyError as e:
        print(f"Database error in delete_alert_rule: {e}")
        session.rollback()
        return None
