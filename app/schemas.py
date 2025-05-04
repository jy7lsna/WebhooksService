from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Webhook Payload Schema ---

class WebhookPayload(BaseModel):
    user_id: int
    event_type: List[str]
    timestamp: Optional[datetime] = None
    data: Optional[Dict[str, Any]] = None

# --- Subscriptions Schemas ---

class SubscriptionBase(BaseModel):
    target_url: str
    secret: Optional[str] = None
    event_type: Optional[List[str]] = Field(default_factory=list)

    class Config:
        from_attributes = True
        validate_by_name = True  # For Pydantic v2

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    pass

class SubscriptionOut(SubscriptionBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        validate_by_name = True  # For Pydantic v2

# --- Delivery Log Schemas ---

class DeliveryLogBase(BaseModel):
    subscription_id: int
    url: str
    attempt_number: int
    outcome: str
    payload: str
    http_status: Optional[int] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True
        validate_by_name = True

class DeliveryLogCreate(DeliveryLogBase):
    pass

class DeliveryLogOut(DeliveryLogBase):
    id: int 
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
        validate_by_name = True
