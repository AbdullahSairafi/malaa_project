""" Alert Model """

import datetime
from email import message
import uuid
from sqlalchemy import Column, DateTime, Float, String, func
from sqlalchemy.dialects.postgresql import UUID
from db.models.model_base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    symbol = Column(String, nullable=False)
    trigger_price = Column(Float, nullable=False)
    threshold_price = Column(Float, nullable=False)
