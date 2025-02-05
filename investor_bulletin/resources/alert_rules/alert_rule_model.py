""" Alert Rule Model """

import uuid
from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.postgresql import UUID
from db.models.model_base import Base


class AlertRule(Base):
    __tablename__ = "alert-rules"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    threshold_price = Column(Float, nullable=False)
    symbol = Column(String, nullable=False)
