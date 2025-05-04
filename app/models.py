from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    target_url = Column(Text, nullable=False)
    secret = Column(String, nullable=False)  
    event_type = Column(ARRAY(String), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)  # comma-separated event types for filtering

    deliveries = relationship("DeliveryLog", back_populates="subscription")

class DeliveryLog(Base):
    __tablename__ = "DeliveryLog"
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    url = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    attempt_number = Column(Integer, nullable=False)
    outcome = Column(String, nullable=False)  # Success, Failed Attempt, Failure
    http_status = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    payload = Column(Text, nullable=False)  # Store payload for reference

    subscription = relationship("Subscription", back_populates="deliveries")
