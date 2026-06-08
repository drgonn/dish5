# FastAPI 主入口 — dish5
# 基于 dish4 的 lifespan 模式，整合 dish3 的异常处理
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import run_migrations_or_init
from .api.v1.router import api_router
from .tasks import start_scheduler, stop_scheduler

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("dish5")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("dish5 启动中...")

    # 运行数据库迁移
    try:
        await run_migrations_or_init()
        logger.info("数据库迁移完成")
    except Exception as e:
        logger.warning(f"数据库迁移失败: {e}")

    # 启动定时任务
    try:
        start_scheduler()
        logger.info("定时任务已启动")
    except Exception as e:
        logger.error(f"定时任务启动失败: {e}")

    yield

    # 关闭
    logger.info("dish5 关闭中...")
    stop_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST API 路由
app.include_router(api_router, prefix="/api/v1")

# Admin 管理后台（Jinja2）
from .admin import admin_router
app.include_router(admin_router)


@app.get("/")
async def root():
    """根路径 — 健康检查"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
