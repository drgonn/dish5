# 聚合接口 — dish5
# 来自 dish_online 的 dish_group_detail，保留其 merge_and_sum_weights 算法
from collections import defaultdict
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....models.dish import Dish

router = APIRouter()


def merge_and_sum(data: list) -> list:
    """合并同名食材，累加用量。
    来自 dish_online 的 merge_and_sum_weights，适配新的 JSON 字段名。
    注意：用量是字符串（如 "500g"），简单同名合并不解析单位。
    """
    merged = defaultdict(list)
    for item in data:
        name = item.get("name", "")
        if name:
            merged[name].append(item)
    # 保留第一个 item 作为基准，记录重复次数
    result = []
    for name, items in merged.items():
        if len(items) == 1:
            result.append(items[0])
        else:
            # 多个同名食材，合并用量
            combined = dict(items[0])
            amounts = [it.get("amount", "") for it in items if it.get("amount")]
            combined["amount"] = " + ".join(amounts) if amounts else ""
            result.append(combined)
    return result


@router.get("/dishes/aggregate")
async def aggregate_dishes(
    ids: str = Query(..., description="逗号分隔的菜品ID列表"),
    db: AsyncSession = Depends(get_db),
):
    """多选菜品聚合食材/步骤 — 来自 dish_online"""
    id_list = [int(id_) for id_ in ids.split(",") if id_.strip().isdigit()]
    if not id_list:
        return {"success": True, "data": None, "detail": "未提供有效ID"}

    result = await db.execute(select(Dish).where(Dish.id.in_(id_list)))
    dishes = result.scalars().all()

    # 聚合各维度
    main_food = []
    side_food = []
    seasonings_list = []
    cooks = []
    attentions = []
    washes = []
    cuts = []
    salts = []

    for dish in dishes:
        main_food.extend(dish.main_ingredients or [])
        side_food.extend(dish.side_ingredients or [])
        seasonings_list.extend(dish.seasonings or [])
        attentions.extend(dish.attentions or [])

        # 烹饪步骤按菜品分组
        cook = {
            "steps": [s.get("name", "") for s in (dish.cooking_steps or [])],
            "attentions": [a.get("name", "") for a in (dish.attentions or [])],
            "name": dish.name,
        }
        cooks.append(cook)

        # 备菜按 act 分类
        for p in (dish.prep_steps or []):
            act = p.get("act", "")
            if act == "洗":
                washes.append(p)
            elif act == "切":
                cuts.append(p)
            elif act == "腌":
                salts.append(p)

    return {
        "success": True,
        "data": {
            "main_food": merge_and_sum(main_food),
            "side_food": merge_and_sum(side_food),
            "seasonings": merge_and_sum(seasonings_list),
            "attentions": attentions,
            "cooks": cooks,
            "washes": washes,
            "cuts": cuts,
            "salts": salts,
        },
    }
