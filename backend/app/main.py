import logging, time, os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .core.config import settings
from .core.database import run_migrations_or_init
from .api.v1.router import api_router
from .tasks import start_scheduler, stop_scheduler

logger = logging.getLogger("dish5")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("dish5 启动中...")
    await run_migrations_or_init()
    logger.info("数据库迁移完成")
    start_scheduler()
    logger.info("定时任务已启动")
    yield
    logger.info("dish5 关闭中...")
    stop_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    dt = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({dt:.0f}ms)")
    return response


app.include_router(api_router, prefix="/api/v1")
from .admin import admin_router
app.include_router(admin_router)


# 生产环境：serve 前端静态文件 + SPA fallback
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if os.path.isdir(STATIC_DIR):
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
