""" Alert Schema """

"""_summary_
This file to abstract any validation logic for the Alerts
"""
from uuid import UUID
from pydantic import BaseModel


class AlertCreate(BaseModel):
    symbol: str
    trigger_price: float
    threshold_price: float


class AlertResponse(AlertCreate):
    id: UUID

    model_config = {"from_attributes": True}
