<<<<<<< HEAD
FROM python:3.13-slim
=======
FROM python:3.11-slim
>>>>>>> 65cd0d2 (Initial Commit)

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY celery_worker.py .

<<<<<<< HEAD
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5432"]

=======
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 65cd0d2 (Initial Commit)
