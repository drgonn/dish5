FROM python:3.12-slim

WORKDIR /home/dron/projects/dish/dish5/backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY alembic.ini ./
COPY alembic/ ./alembic/

EXPOSE 8000
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
