import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Jesusitrustu123!@db:5432/webhooks")
REDIS_URL = os.getenv("REDIS_URL", "redis://:ZNLKvVMt48yzpiEjH25z1Sti5ayH7rif@redis-16500.c81.us-east-1-2.ec2.redns.redis-cloud.com:16500/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/webhooks")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")  # fallback secret
MAX_RETRIES = 5
RETRY_DELAYS = [10, 30, 60, 300, 900]  # seconds: 10s, 30s, 1m, 5m, 15m
LOG_RETENTION_HOURS = 72
