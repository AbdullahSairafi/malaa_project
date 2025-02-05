from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import get_db
from resources.alerts.alert_schema import AlertResponse
from resources.alerts import alert_service

router = APIRouter(prefix="/alerts")


@router.get("/", response_model=list[AlertResponse])
def get_alerts(offset: int = 0, limit: int = 10, session: Session = Depends(get_db)):
    return alert_service.get_alerts(offset, limit, session)


@router.get("/trigger-alerts", response_model=list[AlertResponse])
def trigger_alerts(session: Session = Depends(get_db)):
    return alert_service.trigger_alert_creation(session)
