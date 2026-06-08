# Alembic 迁移环境 — dish5
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# 将 backend 目录加入路径，以便导入 app 包
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings
from app.models.base import Base
# 导入所有模型，确保 register 到 Base.metadata
import app.models  # noqa: F401

# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    """从 Settings 获取同步数据库 URL（迁移用 psycopg2/pymysql 等同步驱动）"""
    url = settings.DATABASE_URL
    # asyncpg → psycopg2 用于迁移
    return url.replace("+asyncpg", "+psycopg2")


def run_migrations_offline():
    """离线迁移"""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """在线迁移"""
    connectable = engine_from_config(
        {"sqlalchemy.url": get_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
