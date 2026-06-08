# 购物清单 API — dish5
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas import BaseResponse
from ....crud import crud_daily

router = APIRouter()


@router.get("/{target_date}", response_model=BaseResponse)
async def get_shopping_list(
    target_date: date, db: AsyncSession = Depends(get_db)
):
    """获取指定日期的购物清单"""
    recommend = await crud_daily.get_by_date(db, target_date)
    if not recommend:
        return BaseResponse(detail=f"{target_date} 的推荐不存在", data=None)
    return BaseResponse(data=recommend.shopping_list)


@router.put("/{target_date}", response_model=BaseResponse)
async def update_shopping_list(
    target_date: date,
    items: list[dict],
    db: AsyncSession = Depends(get_db),
):
    """更新购物清单已购状态"""
    recommend = await crud_daily.get_by_date(db, target_date)
    if not recommend:
        raise HTTPException(status_code=404, detail=f"{target_date} 的推荐不存在")

    # 合并更新的 bought 状态
    current_list = recommend.shopping_list or []
    item_map = {item["name"]: item for item in current_list}
    for new_item in items:
        name = new_item.get("name")
        if name in item_map:
            item_map[name]["bought"] = new_item.get("bought", False)

    recommend.shopping_list = list(item_map.values())
    db.add(recommend)
    await db.flush()
    await db.refresh(recommend)

    return BaseResponse(data=recommend.shopping_list, detail="更新成功")
