""" Alert Rule Schema """

"""_summary_
This file to abstract any validation logic for the Alert Rules
"""
from pydantic import BaseModel
from uuid import UUID


class AlertRuleBase(BaseModel):
    name: str
    threshold_price: float
    symbol: str


class AlertRuleCreate(AlertRuleBase):
    pass


class AlertRuleUpdate(AlertRuleBase):
    name: str | None = None
    threshold_price: float | None = None
    symbol: str | None = None


class AlertRuleResponse(AlertRuleBase):
    id: UUID

    model_config = {"from_attributes": True}
