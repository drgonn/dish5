# 数据库连接配置 — dish5
# 异步 PostgreSQL，配合 Alembic 迁移
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import settings

logger = logging.getLogger("dish5.database")

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass


async def get_db() -> AsyncSession:
    """FastAPI 依赖：获取数据库会话"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def run_migrations_or_init():
    """启动时运行 Alembic 迁移，失败则回退到 create_all"""
    try:
        from alembic.config import Config
        from alembic import command
        import os

        alembic_cfg = Config(
            os.path.join(os.path.dirname(__file__), "..", "..", "alembic.ini")
        )
        # 覆盖 URL，确保用异步驱动
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        command.upgrade(alembic_cfg, "head")
        logger.info("Alembic 迁移完成")
    except Exception as e:
        logger.warning(f"Alembic 迁移失败 ({e})，回退到 create_all")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("create_all 完成（回退模式）")
