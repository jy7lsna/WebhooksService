from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional

def get_subscription(db: Session, subscription_id: int) -> Optional[models.Subscription]:
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

def get_subscriptions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Subscription]:
    return db.query(models.Subscription).offset(skip).limit(limit).all()

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate) -> models.Subscription:
    db_sub = models.Subscription(
        target_url=subscription.target_url, 
        secret=subscription.secret, 
        event_type=subscription.event_type  # adjust if your model uses event_types
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def update_subscription(db: Session, subscription_id: int, subscription: schemas.SubscriptionUpdate) -> Optional[models.Subscription]:
    db_sub = get_subscription(db, subscription_id)
    if not db_sub:
        return None
    db_sub.target_url = subscription.target_url
    db_sub.secret = subscription.secret
    db_sub.event_type = subscription.event_type  # adjust if your model uses event_types
    db.commit()
    db.refresh(db_sub)
    return db_sub

def delete_subscription(db: Session, subscription_id: int) -> bool:
    db_sub = get_subscription(db, subscription_id)
    if not db_sub:
        return False
    db.delete(db_sub)
    db.commit()
    return True

def create_delivery_log(
    db: Session, 
    subscription_id: int, 
    target_url: str, 
    attempt_number: int, 
    outcome: str, 
    payload: str, 
    http_status: int = None, 
    error: str = None
):
    log = models.DeliveryLog(
        subscription_id=subscription_id,
        target_url=target_url,
        attempt_number=attempt_number,
        outcome=outcome,
        http_status=http_status,
        error=error,
        payload=payload
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_delivery_logs_by_subscription(db: Session, subscription_id: int, limit: int = 20):
    return (
        db.query(models.DeliveryLog)
        .filter(models.DeliveryLog.subscription_id == subscription_id)
        .order_by(models.DeliveryLog.timestamp.desc())
        .limit(limit)
        .all()
    )

def get_delivery_log(db: Session, delivery_id: int):
    return db.query(models.DeliveryLog).filter(models.DeliveryLog.id == delivery_id).first()

def delete_old_logs(db: Session, older_than_hours: int) -> int:
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(hours=older_than_hours)
    deleted = (
        db.query(models.DeliveryLog)
        .filter(models.DeliveryLog.timestamp < cutoff)
        .delete(synchronize_session=False)
    )
    db.commit()
    return deleted
