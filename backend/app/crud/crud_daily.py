# 每日推荐 CRUD — dish5
from datetime import date
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD
from ..models.daily_recommend import DailyRecommend


class CRUDDaily(BaseCRUD):
    def __init__(self):
        super().__init__(DailyRecommend)

    async def get_by_date(
        self, db: AsyncSession, target_date: date
    ) -> Optional[DailyRecommend]:
        """按日期获取推荐记录"""
        result = await db.execute(
            select(DailyRecommend).where(DailyRecommend.date == target_date)
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        db: AsyncSession,
        *,
        target_date: date,
        recipes: list,
        shopping_list: list,
        aggregated: dict,
    ) -> DailyRecommend:
        """创建或更新每日推荐"""
        existing = await self.get_by_date(db, target_date)
        if existing:
            existing.recipes = recipes
            existing.shopping_list = shopping_list
            existing.aggregated = aggregated
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            return existing
        else:
            db_obj = DailyRecommend(
                date=target_date,
                recipes=recipes,
                shopping_list=shopping_list,
                aggregated=aggregated,
            )
            db.add(db_obj)
            await db.flush()
            await db.refresh(db_obj)
            return db_obj

    async def mark_notified(self, db: AsyncSession, id: int) -> None:
        """标记已推送通知"""
        result = await db.execute(
            select(DailyRecommend).where(DailyRecommend.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            from datetime import datetime
            obj.notified = True
            obj.notified_at = datetime.now()
            db.add(obj)
            await db.flush()


crud_daily = CRUDDaily()
