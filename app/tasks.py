from celery import Celery
import requests
from fastapi.encoders import jsonable_encoder
import json
from pydantic import BaseModel
from app.config import MAX_RETRIES
from app.database import SessionLocal 
from app import crud, utils
from celery.utils.log import get_task_logger
import os
from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.environ["REDIS_URL"]

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)
logger = get_task_logger(__name__)

@celery.task(bind=True, max_retries=MAX_RETRIES)
def deliver_webhook(self, subscription_id: int, payload: dict, attempt_number: int = 1):
    db = SessionLocal()
    try:
        subscription = crud.get_subscription(db, subscription_id)
        if not subscription:
            logger.error(f"Subscription {subscription_id} not found")
            return

        target_url = subscription.target_url
        secret = subscription.secret
        headers = {"Content-Type": "application/json"}

        # Prepare payload for signature and sending
        if isinstance(payload, BaseModel):
            payload_data = payload.dict()
            raw_payload = json.dumps(payload_data, separators=(',', ':')).encode()
            json_payload = payload.json()
        else:
            payload_data = payload
            raw_payload = json.dumps(payload_data, separators=(',', ':')).encode()
            json_payload = json.dumps(jsonable_encoder(payload_data))

        # Optional: Add signature header if secret exists
        if secret:
            import hmac, hashlib
            signature = hmac.new(secret.encode(), raw_payload, hashlib.sha256).hexdigest()
            headers["X-Hub-Signature-256"] = f"sha256={signature}"

        # Deliver webhook
        response = requests.post(target_url, data=json_payload, headers=headers, timeout=10)
        status_code = response.status_code

        if 200 <= status_code < 300:
            outcome = "Success"
            crud.create_delivery_log(
                db,
                subscription_id,
                target_url,
                attempt_number,
                outcome,
                json_payload,
                http_status=status_code
            )
            db.commit()
            logger.info(f"Delivered webhook to {target_url} successfully")
        else:
            raise Exception(f"Non-2xx response: {status_code}")

    except Exception as exc:
        outcome = "Failed Attempt" if attempt_number < MAX_RETRIES else "Failure"
        error_msg = str(exc)
        crud.create_delivery_log(
            db, 
            subscription_id, 
            subscription.target_url if subscription else "unknown", 
            attempt_number, 
            outcome, 
            json_payload if 'json_payload' in locals() else json.dumps(payload), 
            error=error_msg
        )
        db.commit()
        logger.error(f"Delivery attempt {attempt_number} failed: {error_msg}")

        if attempt_number < MAX_RETRIES:
            delay = utils.get_retry_delay(attempt_number)
            raise self.retry(countdown=delay, exc=exc)
        else:
            logger.error(f"Max retries reached for subscription {subscription_id}")
    finally:
        db.close()
