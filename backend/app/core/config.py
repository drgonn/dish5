# 核心配置 — dish5
# 基于 dish4 的 pydantic-settings 模式，保留 dish3 的 ${VAR:-default} 环境变量展开能力
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "dish5 - 菜谱推荐系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # PostgreSQL 数据库配置
    PG_HOST: str = "localhost"
    PG_PORT: int = 5434
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DATABASE: str = "dish5"

    # 数据库连接 URL（优先使用环境变量 DATABASE_URL）
    @property
    def DATABASE_URL(self) -> str:
        if os.environ.get("DATABASE_URL"):
            url = os.environ["DATABASE_URL"]
            return url.replace("postgres://", "postgresql+asyncpg://")
        return (
            f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DATABASE}"
        )

    # 定时任务 — 每日推荐时间
    RECOMMEND_HOUR: int = 8
    RECOMMEND_MINUTE: int = 0

    # 通知 — 企业微信 Webhook URL（从环境变量读取，避免硬编码）
    NOTIFICATION_WEBHOOK_URL: Optional[str] = None

    # CORS
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
