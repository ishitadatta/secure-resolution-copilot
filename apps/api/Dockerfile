FROM python:3.12-slim

WORKDIR /app
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt psycopg[binary]==3.2.9

COPY apps/api/app ./app
COPY evals /evals

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
