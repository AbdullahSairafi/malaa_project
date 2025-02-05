""" Alert Rule Service"""

"""_summary_
this file to write any business logic for the Alert Rules
"""
from uuid import UUID
from resources.alert_rules.alert_rule_schema import (
    AlertRuleBase,
    AlertRuleCreate,
    AlertRuleResponse,
    AlertRuleUpdate,
)

# from resources.alert_rules.alert_rule_dal import create_alert_rule
from resources.alert_rules import alert_rule_dal as rule_repository
from sqlalchemy.orm import Session


def create_alert_rule(rule: AlertRuleCreate, session: Session) -> AlertRuleResponse:
    db_rule = rule_repository.create_alert_rule(rule, session)
    if not db_rule:
        return None
    return AlertRuleResponse.model_validate(db_rule)  # convert from model to schema


def get_alert_rule(rule_id: UUID, session: Session) -> AlertRuleResponse:
    db_rule = rule_repository.get_alert_rule(rule_id, session)
    if not db_rule:
        return None
    return AlertRuleResponse.model_validate(db_rule)


def get_alert_rules(
    offset: int, limit: int, session: Session
) -> list[AlertRuleResponse]:

    db_rules = rule_repository.get_alert_rules(offset, limit, session)

    if not db_rules:
        return []

    rules = []

    for db_rule in db_rules:  # populate list with converted rules (model to schema)
        rules.append(AlertRuleResponse.model_validate(db_rule))

    return rules


def update_alert_rule(
    rule_id: UUID, rule_schema: AlertRuleUpdate, session: Session
) -> AlertRuleResponse:
    db_rule = rule_repository.update_alert_rule(rule_id, rule_schema, session)
    if not db_rule:
        return None

    return AlertRuleResponse.model_validate(db_rule)


def delete_alert_rule(rule_id: UUID, session: Session) -> AlertRuleResponse:
    db_rule = rule_repository.delete_alert_rule(rule_id, session)
    if not db_rule:
        return None

    return AlertRuleResponse.model_validate(db_rule)


def get_all_alert_rules(session: Session) -> list[AlertRuleResponse]:
    rules = []
    offset = 0
    limit = 100
    while True:
        data = get_alert_rules(offset=offset, limit=limit, session=session)
        if not data:
            break

        # add records to list (individually) hence extend() instead of append()
        rules.extend(data)
        offset += limit

    return rules
