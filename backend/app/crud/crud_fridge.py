# 冰箱 CRUD — dish5
from typing import Optional, List
from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD
from ..models.fridge_item import FridgeItem


class CRUDFridge(BaseCRUD):
    def __init__(self):
        super().__init__(FridgeItem)

    async def get_by_name(
        self, db: AsyncSession, user_id: int, ingredient_name: str
    ) -> Optional[FridgeItem]:
        result = await db.execute(
            select(FridgeItem).where(
                FridgeItem.user_id == user_id,
                FridgeItem.ingredient_name == ingredient_name,
            )
        )
        return result.scalar_one_or_none()

    async def get_all_names(self, db: AsyncSession, user_id: int) -> List[str]:
        """获取用户冰箱中所有食材名（用于匹配）"""
        result = await db.execute(
            select(FridgeItem.ingredient_name).where(FridgeItem.user_id == user_id)
        )
        return [row[0] for row in result.all()]

    async def get_by_category(
        self, db: AsyncSession, user_id: int, category: Optional[str] = None
    ) -> List[FridgeItem]:
        query = select(FridgeItem).where(FridgeItem.user_id == user_id)
        if category:
            query = query.where(FridgeItem.category == category)
        query = query.order_by(FridgeItem.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def add_or_update(
        self, db: AsyncSession, *, user_id: int, ingredient_name: str,
        category: str = "其他", quantity: str = "", added_from: str = "manual"
    ) -> FridgeItem:
        existing = await self.get_by_name(db, user_id, ingredient_name)
        if existing:
            existing.quantity = quantity or existing.quantity
            existing.category = category or existing.category
            existing.added_from = added_from
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            return existing
        else:
            return await self.create(db, obj_in={
                "user_id": user_id,
                "ingredient_name": ingredient_name,
                "category": category,
                "quantity": quantity,
                "added_from": added_from,
            })

    async def batch_add(
        self, db: AsyncSession, user_id: int, names: List[str]
    ) -> int:
        count = 0
        for name in names:
            existing = await self.get_by_name(db, user_id, name)
            if not existing:
                await self.create(db, obj_in={
                    "user_id": user_id,
                    "ingredient_name": name,
                    "added_from": "shopping",
                })
                count += 1
        return count

    async def remove_by_name(
        self, db: AsyncSession, user_id: int, ingredient_name: str
    ) -> bool:
        result = await db.execute(
            sql_delete(FridgeItem).where(
                FridgeItem.user_id == user_id,
                FridgeItem.ingredient_name == ingredient_name,
            )
        )
        await db.flush()
        return result.rowcount > 0


crud_fridge = CRUDFridge()
