from celery import Celery
import requests
<<<<<<< HEAD
from fastapi.encoders import jsonable_encoder
import json
from pydantic import BaseModel
from app.config import MAX_RETRIES
from app.database import SessionLocal 
from app import crud, utils, models, schemas
import json
from celery.utils.log import get_task_logger
import os
from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.environ["REDIS_URL"]

=======
from app.config import REDIS_URL, MAX_RETRIES
from app.database import SessionLocal
from app import crud, utils
import json
from celery.utils.log import get_task_logger
>>>>>>> 65cd0d2 (Initial Commit)

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)
logger = get_task_logger(__name__)

@celery.task(bind=True, max_retries=MAX_RETRIES)
<<<<<<< HEAD
def deliver_webhook(self, subscription_id: int, payload: dict, attempt_number: int = 1):
=======
def deliver_webhook(self, subscription_id: str, payload: dict, attempt_number: int = 1):
>>>>>>> 65cd0d2 (Initial Commit)
    db = SessionLocal()
    try:
        subscription = crud.get_subscription(db, subscription_id)
        if not subscription:
<<<<<<< HEAD
            logger.error(f"subscriptions {subscription_id} not found")
            return

        target_url = subscription.target_url
=======
            logger.error(f"Subscription {subscription_id} not found")
            return

        url = subscription.target_url
>>>>>>> 65cd0d2 (Initial Commit)
        secret = subscription.secret
        headers = {"Content-Type": "application/json"}

        # Optional: Add signature header if secret exists
        if secret:
            import hmac, hashlib
<<<<<<< HEAD
            raw_payload = json.dumps(payload.model_dump(), separators=(',', ':')).encode()            
=======
            raw_payload = json.dumps(payload).encode()
>>>>>>> 65cd0d2 (Initial Commit)
            signature = hmac.new(secret.encode(), raw_payload, hashlib.sha256).hexdigest()
            headers["X-Hub-Signature-256"] = f"sha256={signature}"

        # Deliver webhook
<<<<<<< HEAD
        response = requests.post(target_url, json_payload = payload.json(), headers=headers, timeout=10)
=======
        response = requests.post(url, json=payload, headers=headers, timeout=10)
>>>>>>> 65cd0d2 (Initial Commit)
        status_code = response.status_code

        if 200 <= status_code < 300:
            outcome = "Success"
<<<<<<< HEAD
            if isinstance(payload, BaseModel):
                json_payload = payload.json()
            else:
                json_payload = json.dumps(jsonable_encoder(payload))

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
=======
            crud.create_delivery_log(db, subscription_id, url, attempt_number, outcome, json.dumps(payload), http_status=status_code)
            logger.info(f"Delivered webhook to {url} successfully")
        else:
            raise Exception(f"Non-2xx response: {status_code}")
>>>>>>> 65cd0d2 (Initial Commit)

    except Exception as exc:
        outcome = "Failed Attempt" if attempt_number < MAX_RETRIES else "Failure"
        error_msg = str(exc)
<<<<<<< HEAD
        crud.create_delivery_log(
            db, 
            subscription_id, 
            subscription.target_url if subscription else "unknown", 
            attempt_number, 
            outcome, 
            payload.json(), 
            error=error_msg)
        db.commit()
=======
        crud.create_delivery_log(db, subscription_id, subscription.target_url if subscription else "unknown", attempt_number, outcome, json.dumps(payload), error=error_msg)
>>>>>>> 65cd0d2 (Initial Commit)
        logger.error(f"Delivery attempt {attempt_number} failed: {error_msg}")

        if attempt_number < MAX_RETRIES:
            delay = utils.get_retry_delay(attempt_number)
            raise self.retry(countdown=delay, exc=exc)
        else:
            logger.error(f"Max retries reached for subscription {subscription_id}")
    finally:
        db.close()
