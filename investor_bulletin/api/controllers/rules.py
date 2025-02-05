from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.models import get_db
from resources.alert_rules.alert_rule_schema import (
    AlertRuleBase,
    AlertRuleCreate,
    AlertRuleResponse,
    AlertRuleUpdate,
)
from resources.alert_rules import alert_rule_service as rule_service

router = APIRouter(prefix="/alert-rules")


@router.get("/test")
def test_db_connection(session: Session = Depends(get_db)):
    try:
        session.execute(text("SELECT 1"))  # Simple query to test DB connection
        return {"status": "Database connected successfully!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}


@router.post("/", response_model=AlertRuleResponse)
def create_alert_rule(rule: AlertRuleCreate, session: Session = Depends(get_db)):
    rule = rule_service.create_alert_rule(rule, session)
    if not rule:
        raise HTTPException(status_code=500, detail="Failed to create Alert Rule")
    return rule


@router.get("/{id}", response_model=AlertRuleResponse)
def get_alert_rule(id: UUID, session: Session = Depends(get_db)):
    rule = rule_service.get_alert_rule(id, session)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert Rule not found")
    return rule


@router.get("/", response_model=list[AlertRuleResponse])
def get_alert_rules(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_db)
):
    rules = rule_service.get_alert_rules(offset, limit, session)
    return rules


@router.patch("/{id}", response_model=AlertRuleResponse)
def update_alert_rule(
    id: UUID, rule_schema: AlertRuleUpdate, session: Session = Depends(get_db)
):
    rule = rule_service.update_alert_rule(id, rule_schema, session)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert Rule not found")
    return rule


@router.delete("/{id}", response_model=AlertRuleResponse)
def delete_alert_rule(id: UUID, session: Session = Depends(get_db)):
    rule = rule_service.delete_alert_rule(id, session)
    if not rule:
        raise HTTPException(status_code=404, detail="Alert Rule not found")
    return rule
