# 收藏 CRUD — dish5
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD
from ..models.favorite import Favorite


class CRUDFavorite(BaseCRUD):
    def __init__(self):
        super().__init__(Favorite)

    async def get_user_favorite(
        self, db: AsyncSession, user_id: int, dish_id: int
    ) -> Optional[Favorite]:
        """检查用户是否已收藏某菜品"""
        result = await db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.dish_id == dish_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_user_favorites(
        self, db: AsyncSession, user_id: int
    ) -> List[Favorite]:
        """获取用户所有收藏"""
        result = await db.execute(
            select(Favorite)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
        )
        return list(result.scalars().all())


crud_favorite = CRUDFavorite()
