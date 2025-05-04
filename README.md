# Webhook Delivery Service

A robust, containerized backend system for reliable webhook delivery with retries, logging, caching, and status APIs.

---

## 🚀 Live Demo

[**Live Deployed Application**](https://your-deployment-url.com)  
--- In process 
<video src="https://github.com/yourusername/yourrepo](https://github.com/jy7lsna/WebhooksService/assets/recording.mp4" controls width="600"></video>


## 🐳 Quick Start: Running Locally with Docker

### **Prerequisites**
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed

### **1. Clone the Repository**
```git clone https://github.com/jy7lsna/WebhooksService.git```
```cd WebhooksService```


### **2. Copy the Example Environment File**
```cp .env.example .env```

Edit `.env` to set your database/Redis credentials if needed.

### **3. Build and Start the Stack**
```docker-compose up --build```

This will start:
- FastAPI API server
- Celery worker
- PostgreSQL database
- Redis (for caching and Celery broker)

### **4. Access the Application**
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Minimal UI: [http://localhost:8000/](http://localhost:8000/)

---

## 🛠️ Architecture Choices

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python) for async, type-safe APIs and automatic docs.
- **Database:** [PostgreSQL](https://www.postgresql.org/) for relational data (subscriptions, delivery logs); supports indexing and large volumes.
- **Async Task Queue:** [Celery](https://docs.celeryq.dev/) with Redis as broker/result backend for robust background processing and retries.
- **Caching:** [Redis](https://redis.io/) for fast subscription lookups by workers.
- **Containerization:** Docker & Docker Compose for reproducible local and cloud deployment.
- **Retry Strategy:** Celery’s built-in retry with exponential backoff (10s, 30s, 1m, 5m, 15m; max 5 attempts).
- **Log Retention:** Periodic Celery task deletes delivery logs older than 72 hours.
- **Minimal UI:** FastAPI’s `/docs` (Swagger) and a simple HTML homepage.

---

## 🗄️ Database Schema & Indexing

- **subscriptions**
  - `id` (PK, indexed)
  - `target_url` (indexed)
  - `secret` (nullable)
  - `event_type` (array of strings)
- **delivery_logs**
  - `id` (PK, UUID, indexed)
  - `subscription_id` (FK, indexed)
  - `target_url`
  - `timestamp` (indexed)
  - `attempt_number`
  - `outcome` (Success, Failed Attempt, Failure)
  - `http_status`
  - `error_details`
- **Indexes:**  
  - On `subscription_id`, `timestamp` in `delivery_logs` for fast lookups.
  - On `target_url` in `subscriptions` for efficient querying.

---

## 📋 API Usage Examples (cURL)

### **Create a Subscription**
```curl -X POST http://localhost:8000/subscriptions```
```-H "Content-Type: application/json"```
```-d '{"target_url":"https://webhook.site/your-url","event_type":["order.created"],"secret":"mysecret"}'```


### **List Subscriptions**
```curl http://localhost:8000/subscriptions```

### **Update a Subscription**
```curl -X PUT http://localhost:8000/subscriptions/1```
```-H "Content-Type: application/json"```
```-d '{"target_url":"https://webhook.site/your-new-url","event_type":["order.updated"]}'```


### **Delete a Subscription**
```curl -X DELETE http://localhost:8000/subscriptions/1```


### **Ingest a Webhook**
```curl -X POST http://localhost:8000/ingest/1```
-H "Content-Type: application/json"```
```-H "X-Hub-Signature-256: sha256=..."```
```-H "event_type: order.created"```
```-d '{"order_id":123,"amount":49.99}'```


### **Check Delivery Status**
```curl http://localhost:8000/status/<delivery_id>```


### **Get Recent Logs for a Subscription**
```curl http://localhost:8000/subscriptions/1/logs```

## 📝 Assumptions

- All endpoints are authenticated only if needed (add auth in production).
- Webhook payloads are JSON and < 1MB.
- Free tier resources are sufficient for moderate traffic and log retention.
- Email notifications, advanced analytics, and UI polish are out of scope.

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [Render](https://render.com/) / [Heroku](https://heroku.com/) (for deployment)
- [OpenAI / Perplexity AI](https://www.perplexity.ai/) (for AI assistance)
- Perplexity AI


##🧪 Testing
- Use `pytest` for unit/integration tests (see `/tests` folder).
