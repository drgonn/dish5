# 通用 CRUD 基类 — dish5
# 消除 dish3 中每个实体 150+ 行的重复 CRUD 代码
# 基于 dish4 CRUD 模式，提取公共逻辑
from typing import Optional, List, Tuple, Type, Any, Dict, Set
from sqlalchemy import select, func, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import asc, desc


class BaseCRUD:
    """通用 CRUD 基类。
    使用方式:
        crud_dish = BaseCRUD[Dish](Dish)
        item, total = await crud_dish.get_multi(db, skip=0, limit=20, ...)
    """

    def __init__(self, model: Type):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[Any]:
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        sort_field: Optional[str] = None,
        sort_order: str = "desc",
        allowed_sort_fields: Optional[Set[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Tuple[List[Any], int]:
        """分页列表查询，支持排序白名单和动态筛选"""
        base_query = select(self.model)
        count_query = select(func.count(self.model.id))

        # 应用筛选条件
        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(self.model, field):
                    col = getattr(self.model, field)
                    if isinstance(value, str):
                        base_query = base_query.where(col.like(f"%{value}%"))
                        count_query = count_query.where(col.like(f"%{value}%"))
                    else:
                        base_query = base_query.where(col == value)
                        count_query = count_query.where(col == value)

        # 总数
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # 排序 — 白名单校验（来自 dish3 的安全模式）
        if sort_field and allowed_sort_fields and sort_field in allowed_sort_fields:
            col = getattr(self.model, sort_field)
            base_query = base_query.order_by(
                asc(col) if sort_order == "asc" else desc(col)
            )

        # 分页
        base_query = base_query.offset(skip).limit(limit)
        result = await db.execute(base_query)
        items = list(result.scalars().all())

        return items, total

    async def create(self, db: AsyncSession, *, obj_in: Dict[str, Any]) -> Any:
        """创建记录"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Any, obj_in: Dict[str, Any]
    ) -> Any:
        """部分更新 — 只更新传入的字段"""
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> bool:
        """删除单条"""
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if db_obj:
            await db.delete(db_obj)
            await db.flush()
            return True
        return False

    async def delete_batch(self, db: AsyncSession, *, ids: List[int]) -> int:
        """批量删除，返回删除数量"""
        if not ids:
            return 0
        result = await db.execute(
            sql_delete(self.model).where(self.model.id.in_(ids))
        )
        await db.flush()
        return result.rowcount
