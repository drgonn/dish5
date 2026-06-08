# 推荐算法服务 — dish5 V2
# 支持可配置推荐数量，5 级备菜编排
from collections import defaultdict
from datetime import date
from typing import List, Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.dish import Dish
from ..crud import crud_dish, crud_daily, crud_preference

# 备菜优先级排序
PREP_ORDER = ["腌", "泡", "发", "洗", "切", "备"]


class RecommendService:
    """每日菜单推荐服务

    算法：
    1. 读取用户偏好 (meat_count, vegetable_count, soup_count)
    2. 当前月份应季菜品，按 eats ASC 选取
    3. 空类回退
    4. 合并食材 → 购物清单
    5. 5 级备菜编排：腌/泡(耗时) → 洗 → 切 → 备 → 烹
    6. eats += 1, 存入 daily_recommends
    """

    def __init__(self, db: AsyncSession, user_id: int = 1):
        self.db = db
        self.user_id = user_id

    async def generate_daily_menu(self, target_date: date):
        """生成每日推荐，使用用户偏好配置"""
        # 读取偏好
        pref = await crud_preference.get_or_create(self.db, self.user_id)
        meat_count = pref.meat_count
        vegetable_count = pref.vegetable_count
        soup_count = pref.soup_count

        month = target_date.month

        # 获取各类应季菜品
        hard_limit = max(meat_count + 2, 3)
        veg_limit = max(vegetable_count + 2, 4)
        soup_limit = max(soup_count + 1, 2)

        hard_dishes = await crud_dish.get_by_dtype(self.db, "硬菜", month, limit=hard_limit)
        veg_dishes = await crud_dish.get_by_dtype(self.db, "素菜", month, limit=veg_limit)
        meat_soup = await crud_dish.get_by_dtype(self.db, "肉汤", month, limit=soup_limit)
        veg_soup = await crud_dish.get_by_dtype(self.db, "素汤", month, limit=soup_limit)
        soup_dishes = meat_soup + veg_soup

        # 选择菜品
        recommended = []
        used_ids = set()

        def pick(candidates: list, count: int):
            picked = []
            for c in candidates:
                if len(picked) >= count:
                    break
                if c.id not in used_ids:
                    picked.append(c)
                    used_ids.add(c.id)
            return picked

        recommended.extend(pick(hard_dishes, meat_count))
        recommended.extend(pick(veg_dishes, vegetable_count))
        recommended.extend(pick(soup_dishes, soup_count))

        total_needed = meat_count + vegetable_count + soup_count

        # 空类回退
        if len(recommended) < total_needed:
            result = await self.db.execute(
                select(Dish).order_by(Dish.eats.asc()).limit(20)
            )
            all_dishes = list(result.scalars().all())
            for dish in all_dishes:
                if len(recommended) >= total_needed:
                    break
                if dish.id not in used_ids:
                    recommended.append(dish)
                    used_ids.add(dish.id)

        # 生成快照
        recipes_list = [
            {
                "id": r.id,
                "name": r.name,
                "dtype": r.dtype.value if hasattr(r.dtype, "value") else str(r.dtype),
            }
            for r in recommended
        ]

        # 购物清单
        shopping_list = self._generate_shopping_list(recommended)

        # 聚合 + 备菜编排
        aggregated = self._aggregate_dishes(recommended)

        # 存入数据库
        recommend = await crud_daily.create_or_update(
            self.db,
            target_date=target_date,
            recipes=recipes_list,
            shopping_list=shopping_list,
            aggregated=aggregated,
        )

        # 增加食用次数
        for r in recommended:
            await crud_dish.increment_eats(self.db, r.id)

        return recommend

    # ——— 购物清单 ———

    def _generate_shopping_list(self, dishes: List[Dish]) -> List[Dict[str, Any]]:
        ingredients_map: Dict[str, Dict[str, Any]] = {}

        for dish in dishes:
            for ing_list in [
                dish.main_ingredients or [],
                dish.side_ingredients or [],
                dish.seasonings or [],
            ]:
                for ing in ing_list:
                    name = ing.get("name", "").strip()
                    if not name:
                        continue
                    if name not in ingredients_map:
                        ingredients_map[name] = {
                            "name": name,
                            "amount": ing.get("amount", ""),
                            "bought": False,
                        }

        return list(ingredients_map.values())

    # ——— 5 级备菜编排 ———

    def _aggregate_dishes(self, dishes: List[Dish]) -> Dict[str, Any]:
        """聚合 + 智能备菜编排"""
        all_main = []
        all_side = []
        all_seasonings = []
        cooks = []
        all_attentions = []

        # 收集备菜步骤
        prep_steps: Dict[str, Dict] = {}  # key: act, value: {items, time_minutes, notes}

        for dish in dishes:
            all_main.extend(dish.main_ingredients or [])
            all_side.extend(dish.side_ingredients or [])
            all_seasonings.extend(dish.seasonings or [])
            all_attentions.extend(dish.attentions or [])

            cooks.append({
                "name": dish.name,
                "cooking_time": dish.cooking_time,
                "difficulty": dish.difficulty.value if hasattr(dish.difficulty, "value") else str(dish.difficulty),
                "steps": [
                    s.get("name", "") for s in (dish.cooking_steps or [])
                ],
                "attentions": [
                    a.get("name", "") for a in (dish.attentions or [])
                ],
            })

            # 收集并合并备菜步骤
            for p in (dish.prep_steps or []):
                act = p.get("act", "备")
                if act not in prep_steps:
                    prep_steps[act] = {"act": act, "items": [], "time_minutes": 0, "notes": []}

                # 合并 items
                for item in p.get("items", []):
                    name = item.get("name", "")
                    existing = next((i for i in prep_steps[act]["items"] if i["name"] == name), None)
                    if existing:
                        # 合并用量
                        ea = existing.get("amount", "")
                        ia = item.get("amount", "")
                        if ia and ia != ea:
                            existing["amount"] = f"{ea} + {ia}" if ea else ia
                    else:
                        prep_steps[act]["items"].append(dict(item))

                # 累加时间
                t = p.get("time_minutes", 0)
                if t:
                    prep_steps[act]["time_minutes"] = max(prep_steps[act]["time_minutes"], t)

                # 合并备注
                n = p.get("note", "")
                if n and n not in prep_steps[act]["notes"]:
                    prep_steps[act]["notes"].append(n)

        # 按 PREP_ORDER 排序
        def sort_key(item):
            act = item[0]
            try:
                return PREP_ORDER.index(act)
            except ValueError:
                return len(PREP_ORDER)

        sorted_prep = [v for _, v in sorted(prep_steps.items(), key=sort_key)]

        return {
            "main_ingredients": self._merge_ingredients(all_main),
            "side_ingredients": self._merge_ingredients(all_side),
            "seasonings": self._merge_ingredients(all_seasonings),
            "cooking_steps": cooks,
            "attentions": all_attentions,
            "prep_steps": sorted_prep,  # 已按优先级排序
        }

    @staticmethod
    def _merge_ingredients(data: list) -> list:
        merged = defaultdict(list)
        for item in data:
            name = item.get("name", "")
            if name:
                merged[name].append(item.get("amount", ""))
        result = []
        for name, amounts in merged.items():
            result.append({
                "name": name,
                "amount": " + ".join(filter(None, amounts)) if len(amounts) > 1 else amounts[0],
            })
        return result


async def generate_daily_menu_task():
    """定时任务入口：生成每日推荐并发送通知"""
    from ..core.database import AsyncSessionLocal
    import logging

    logger = logging.getLogger("dish5.scheduler")

    async with AsyncSessionLocal() as db:
        service = RecommendService(db)
        today = date.today()

        existing = await crud_daily.get_by_date(db, today)
        if existing:
            logger.info(f"{today} 每日推荐已存在，跳过")
            return existing

        recommend = await service.generate_daily_menu(today)
        logger.info(f"{today} 每日推荐已生成")

        try:
            from .notification import send_notification
            await send_notification(recommend)
        except Exception as e:
            logger.error(f"发送通知失败: {e}")

        return recommend
