from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app import models, schemas, crud, database, tasks, utils, cache
from app.tasks import deliver_webhook
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI(title="Webhook Delivery Service")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    # Initialize Redis connection
    await cache.get_redis()
    models.Base.metadata.create_all(bind=database.engine)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Minimal UI</title>
        <style>
            body { 
            font-family: sans-serif; 
            background: #fafafa; 
            color: #222; display: flex; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0; 
            }
            
            .container { text-align: center; }

            h1 { 
            font-weight: 400; 
            margin-bottom: 1rem;
            }

            button {
            background-color: #007bff;
                border: none;
                color: white;
                padding: 0.6rem 1.2rem;
                font-size: 1rem;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            button:hover {
                background-color: #0056b3;
            }
            a {
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome</h1>
            <p>Webhook Delivery Service</p>
            <a href="/docs"><button>API Docs</button></a>
        </div>
    </body>
    </html>
    """

# subscriptions CRUD
@app.post("/subscriptions", response_model=schemas.SubscriptionOut)
async def create_subscription(sub: schemas.SubscriptionCreate, db: Session = Depends(get_db)):
    db_sub = crud.create_subscription(db, sub)
    await cache.cache_subscription({
        "id": db_sub.id,
        "target_url": db_sub.target_url,
        "secret": db_sub.secret,
        "event_type": db_sub.event_type if db_sub.event_type else []
    })
    return db_sub

@app.get("/subscriptions/{subscription_id}/logs", response_model=list[schemas.DeliveryLogOut])
def get_subscription_logs(subscription_id: int, db: Session = Depends(get_db)):
    logs = crud.get_delivery_logs_by_subscription(db, subscription_id)
    return logs

@app.get("/subscriptions/{subscription_id}", response_model=schemas.SubscriptionOut)
def get_subscription(subscription_id: int, db: Session = Depends(get_db)):
    sub = crud.get_subscription(db, subscription_id)
    if not sub:
        raise HTTPException(status_code=404, detail="subscriptions not found")
    return sub

@app.get("/subscriptions", response_model=list[schemas.SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db)):
    return crud.get_subscriptions(db)

@app.put("/subscriptions/{subscription_id}", response_model=schemas.SubscriptionOut)
async def update_subscription(subscription_id: int, sub: schemas.SubscriptionUpdate, db: Session = Depends(get_db)):
    updated = crud.update_subscription(db, subscription_id, sub)
    if not updated:
        raise HTTPException(status_code=404, detail="subscriptions not found")
    await cache.cache_subscription({
        "id": updated.id,
        "target_url": updated.target_url,
        "secret": updated.secret,
        "event_type": updated.event_type
    })
    return updated


@app.delete("/subscriptions/{subscription_id}")
async def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_subscription(db, subscription_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="subscriptions not found")
    await cache.invalidate_subscription_cache(subscription_id)
    return {"ok": True}

# Webhook ingestion endpoint 
@app.post("/ingest/{subscription_id}")
async def ingest_webhook(
    subscription_id: int,
    payload: schemas.WebhookPayload,
    x_hub_signature_256: str = Header(None),
    event_type: str = Header(None),
    db: Session = Depends(get_db)
        ):
    # Get the raw body for signature verification
    raw_body = json.dumps(payload.model_dump(), separators=(',', ':')).encode('utf-8')

    sub = crud.get_subscription(db, subscription_id)
    if not sub:
        raise HTTPException(status_code=404, detail="subscriptions not found")
    
    print("RAW BODY:", raw_body)
    print("SECRET:", sub.secret)
    print("SIGNATURE HEADER:", x_hub_signature_256)

    # Signature verification: use the exact raw body
    if sub.secret:
        if not utils.verify_signature(sub.secret, raw_body, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Event type filtering: sub.event_type is a list
    if sub.event_type:
        allowed_events = sub.event_type
        if event_type and event_type not in allowed_events:
            raise HTTPException(status_code=403, detail="Event type not subscribed")

    # To queue delivery task asynchronously
    tasks.deliver_webhook.delay(subscription_id, payload.dict(), 1)

    return {
        "subscription_id": subscription_id,
        "payload": payload.dict(),
        "x_hub_signature_256": x_hub_signature_256,
        "event_type": event_type
    }

# Status endpoints
@app.get("/status/{delivery_id}", response_model=schemas.DeliveryLogOut)
def get_delivery_status(delivery_id: str, db: Session = Depends(get_db)):
    log = crud.get_delivery_log(db, delivery_id)
    if not log:
        raise HTTPException(status_code=404, detail="Delivery log not found")
    return log

@app.get("/subscriptions/{subscription_id}/logs", response_model=list[schemas.DeliveryLogOut])
def get_subscription_logs(subscription_id: int, db: Session = Depends(get_db)):
    logs = crud.get_delivery_logs_by_subscription(db, subscription_id)
    return logs
