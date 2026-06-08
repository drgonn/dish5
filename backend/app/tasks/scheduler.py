# 定时调度器 — dish5
# 基于 dish4 的 cron 模式，修复 dish3 的 5 分钟轮询
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..core.config import settings
from ..services.recommend import generate_daily_menu_task

logger = logging.getLogger("dish5.scheduler")

scheduler = AsyncIOScheduler()


def start_scheduler():
    """启动定时任务 — 每天早上 8:00 生成推荐"""
    trigger = CronTrigger(
        hour=settings.RECOMMEND_HOUR,
        minute=settings.RECOMMEND_MINUTE,
        timezone="Asia/Shanghai",
    )
    scheduler.add_job(
        generate_daily_menu_task,
        trigger=trigger,
        id="daily_recommend",
        name="每日推荐生成",
        replace_existing=True,
        misfire_grace_time=300,  # 5 分钟容错
    )
    scheduler.start()
    logger.info(
        f"定时任务已启动: 每日 {settings.RECOMMEND_HOUR:02d}:{settings.RECOMMEND_MINUTE:02d}"
    )


def stop_scheduler():
    """停止定时任务"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("定时任务已停止")
