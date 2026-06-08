# 推荐偏好 CRUD — dish5
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD
from ..models.recommend_preference import RecommendPreference


class CRUDPreference(BaseCRUD):
    def __init__(self):
        super().__init__(RecommendPreference)

    async def get_by_user(
        self, db: AsyncSession, user_id: int
    ) -> Optional[RecommendPreference]:
        result = await db.execute(
            select(RecommendPreference).where(
                RecommendPreference.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_or_create(
        self, db: AsyncSession, user_id: int
    ) -> RecommendPreference:
        pref = await self.get_by_user(db, user_id)
        if not pref:
            pref = await self.create(db, obj_in={"user_id": user_id})
        return pref


crud_preference = CRUDPreference()
