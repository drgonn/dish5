# dish5 — Render 部署用多阶段构建
# Stage 1: 构建前端
FROM node:20-alpine AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --legacy-peer-deps
COPY frontend/ ./
RUN npm run build

# Stage 2: 后端 + 前端静态文件
FROM python:3.12-slim
WORKDIR /home/dron/projects/dish/dish5/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ ./app/
COPY backend/alembic.ini ./
COPY backend/alembic/ ./alembic/
COPY --from=frontend /frontend/dist/build/h5/ ./app/static/

EXPOSE 8000
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
