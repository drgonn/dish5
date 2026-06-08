# 菜品 CRUD — dish5
from typing import Optional, List, Dict, Any
from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseCRUD
from ..models.dish import Dish, DtypeEnum
from ..models.dish_ingredient import DishIngredient


class CRUDDish(BaseCRUD):
    """菜品 CRUD，继承通用基类"""

    def __init__(self):
        super().__init__(Dish)

    # ——— 食材关系表同步 ———

    @staticmethod
    def _extract_ingredient_names(data: Dict[str, Any]) -> List[tuple]:
        """从 dish 数据中提取 (name, type) 用于同步 dish_ingredients"""
        result = []
        for ing_list, ing_type in [
            (data.get("main_ingredients", []), "main"),
            (data.get("side_ingredients", []), "side"),
            (data.get("seasonings", []), "seasoning"),
        ]:
            for item in (ing_list or []):
                name = item.get("name", "").strip() if isinstance(item, dict) else ""
                if name:
                    result.append((name, ing_type))
        return result

    async def _sync_ingredients(self, db: AsyncSession, dish_id: int, data: Dict[str, Any]):
        """同步 dish_ingredients 表"""
        # 删除旧记录
        await db.execute(
            sql_delete(DishIngredient).where(DishIngredient.dish_id == dish_id)
        )
        # 插入新记录
        for name, ing_type in self._extract_ingredient_names(data):
            db.add(DishIngredient(dish_id=dish_id, name=name, type=ing_type))
        await db.flush()

    # ——— CRUD 重写 ———

    async def create(self, db: AsyncSession, *, obj_in: Dict[str, Any]) -> Dish:
        dish = await super().create(db, obj_in=obj_in)
        await self._sync_ingredients(db, dish.id, obj_in)
        return dish

    async def update(
        self, db: AsyncSession, *, db_obj: Dish, obj_in: Dict[str, Any]
    ) -> Dish:
        dish = await super().update(db, db_obj=db_obj, obj_in=obj_in)
        # 合并完整数据再同步（未传入的字段保留原值）
        full_data = {
            "main_ingredients": dish.main_ingredients,
            "side_ingredients": dish.side_ingredients,
            "seasonings": dish.seasonings,
        }
        await self._sync_ingredients(db, dish.id, full_data)
        return dish

    async def delete(self, db: AsyncSession, *, id: int) -> bool:
        # dish_ingredients 由 FK CASCADE 自动删除
        return await super().delete(db, id=id)

    async def delete_batch(self, db: AsyncSession, *, ids: List[int]) -> int:
        return await super().delete_batch(db, ids=ids)

    async def find_by_ingredient(
        self, db: AsyncSession, ingredient_names: List[str],
    ) -> List[Dish]:
        """反向搜索：找出用到指定食材的所有菜品"""
        result = await db.execute(
            select(Dish)
            .join(DishIngredient, Dish.id == DishIngredient.dish_id)
            .where(DishIngredient.name.in_(ingredient_names))
            .distinct()
            .order_by(Dish.eats.asc())
        )
        return list(result.scalars().all())

    async def match_by_fridge(
        self, db: AsyncSession, fridge_names: List[str],
    ) -> List[Dict[str, Any]]:
        """冰箱匹配：按缺失数量排序的菜品列表"""
        # 查询所有菜品及其所需食材
        all_result = await db.execute(
            select(Dish.id, Dish.name, DishIngredient.name, DishIngredient.type)
            .join(DishIngredient, Dish.id == DishIngredient.dish_id)
            .where(DishIngredient.type.in_(["main", "side"]))
        )
        # 按 dish 分组
        dish_ingredients: Dict[int, Dict] = {}
        for dish_id, dish_name, ing_name, ing_type in all_result:
            if dish_id not in dish_ingredients:
                dish_ingredients[dish_id] = {
                    "dish_id": dish_id, "dish_name": dish_name, "ingredients": []
                }
            dish_ingredients[dish_id]["ingredients"].append(ing_name)

        fridge_set = set(fridge_names)
        results = []
        for info in dish_ingredients.values():
            required = set(info["ingredients"])
            if not required:
                continue
            missing = required - fridge_set
            if len(missing) == 0:
                info["match_level"] = "完全可做"
            elif len(missing) <= 2:
                info["match_level"] = f"差{len(missing)}样"
            else:
                info["match_level"] = f"差{len(missing)}样"
                # 仍返回但排序靠后
            info["missing"] = list(missing)
            results.append(info)

        # 排序：完全匹配 > 差1样 > 差2样 > ...
        results.sort(key=lambda x: len(x["missing"]))
        return results

    # ——— 原有方法 ———

    async def get_by_dtype(
        self,
        db: AsyncSession,
        dtype: str,
        month: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Dish]:
        """按类型获取菜品，可选应季筛选，按 eats 升序"""
        try:
            dtype_enum = DtypeEnum(dtype)
        except ValueError:
            return []

        query = select(Dish).where(Dish.dtype == dtype_enum)

        if month is not None:
            query = query.where(
                Dish.start_month <= month,
                Dish.end_month >= month,
            )

        query = query.order_by(Dish.eats.asc())

        if limit is not None:
            query = query.limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def increment_eats(self, db: AsyncSession, dish_id: int) -> None:
        """增加菜品被推荐次数"""
        result = await db.execute(
            select(Dish).where(Dish.id == dish_id)
        )
        dish = result.scalar_one_or_none()
        if dish:
            dish.eats += 1
            db.add(dish)
            await db.flush()


# 单例
crud_dish = CRUDDish()
