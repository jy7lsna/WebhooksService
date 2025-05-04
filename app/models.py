from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
<<<<<<< HEAD
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
=======
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=generate_uuid)
    target_url = Column(String, nullable=False)
    secret = Column(String, nullable=True)
    event_types = Column(String, nullable=True)  # comma-separated event types for filtering
>>>>>>> 65cd0d2 (Initial Commit)

    deliveries = relationship("DeliveryLog", back_populates="subscription")

class DeliveryLog(Base):
<<<<<<< HEAD
    __tablename__ = "DeliveryLog"
    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    url = Column(Text, nullable=False)
=======
    __tablename__ = "delivery_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    subscription_id = Column(String, ForeignKey("subscriptions.id"), nullable=False)
    target_url = Column(String, nullable=False)
>>>>>>> 65cd0d2 (Initial Commit)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    attempt_number = Column(Integer, nullable=False)
    outcome = Column(String, nullable=False)  # Success, Failed Attempt, Failure
    http_status = Column(Integer, nullable=True)
    error = Column(Text, nullable=True)
    payload = Column(Text, nullable=False)  # Store payload for reference

    subscription = relationship("Subscription", back_populates="deliveries")
