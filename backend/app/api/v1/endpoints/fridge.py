# 冰箱 API — dish5
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas import BaseResponse
from ....crud import crud_fridge, crud_dish

router = APIRouter()
DEFAULT_USER_ID = 1


@router.get("", response_model=BaseResponse)
async def list_fridge(
    category: str = Query(None, description="品类筛选"),
    db: AsyncSession = Depends(get_db),
):
    """冰箱库存列表（按品类分组，有的排上面）"""
    items = await crud_fridge.get_by_category(db, DEFAULT_USER_ID, category)
    # 有库存排上面
    sorted_items = sorted(items, key=lambda x: (0 if x.quantity else 1, x.ingredient_name))
    return BaseResponse(data=sorted_items)


@router.post("", response_model=BaseResponse)
async def add_fridge_item(
    ingredient_name: str, category: str = "其他",
    quantity: str = "", added_from: str = "manual",
    db: AsyncSession = Depends(get_db),
):
    """添加食材到冰箱"""
    item = await crud_fridge.add_or_update(
        db, user_id=DEFAULT_USER_ID,
        ingredient_name=ingredient_name, category=category,
        quantity=quantity, added_from=added_from,
    )
    return BaseResponse(data=item, detail="已添加")


@router.post("/batch", response_model=BaseResponse)
async def batch_add(
    names: list[str], db: AsyncSession = Depends(get_db),
):
    """从购物清单一键入库"""
    count = await crud_fridge.batch_add(db, DEFAULT_USER_ID, names)
    return BaseResponse(detail=f"已添加 {count} 种新食材")


@router.delete("/{ingredient_name}", response_model=BaseResponse)
async def remove_fridge_item(
    ingredient_name: str, db: AsyncSession = Depends(get_db),
):
    """从冰箱移除食材（做了菜后扣减）"""
    ok = await crud_fridge.remove_by_name(db, DEFAULT_USER_ID, ingredient_name)
    if not ok:
        raise HTTPException(status_code=404, detail=f"冰箱中没有「{ingredient_name}」")
    return BaseResponse(detail=f"已移除「{ingredient_name}」")


@router.get("/match", response_model=BaseResponse)
async def match_dishes(db: AsyncSession = Depends(get_db)):
    """冰箱匹配：根据库存找出可做的菜"""
    fridge_names = await crud_fridge.get_all_names(db, DEFAULT_USER_ID)
    if not fridge_names:
        return BaseResponse(detail="冰箱是空的，先去买菜吧", data=[])

    results = await crud_dish.match_by_fridge(db, fridge_names)
    return BaseResponse(data=results)
