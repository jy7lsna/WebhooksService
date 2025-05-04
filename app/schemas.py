<<<<<<< HEAD
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
=======
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class SubscriptionBase(BaseModel):
    target_url: HttpUrl
    secret: Optional[str] = None
    event_types: Optional[List[str]] = None  # List of event types
>>>>>>> 65cd0d2 (Initial Commit)

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    pass

class SubscriptionOut(SubscriptionBase):
<<<<<<< HEAD
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
=======
    id: str

    class Config:
        orm_mode = True

class DeliveryLogOut(BaseModel):
    id: str
    subscription_id: str
    target_url: HttpUrl
    timestamp: datetime
    attempt_number: int
    outcome: str
    http_status: Optional[int]
    error: Optional[str]

    class Config:
        orm_mode = True
>>>>>>> 65cd0d2 (Initial Commit)
