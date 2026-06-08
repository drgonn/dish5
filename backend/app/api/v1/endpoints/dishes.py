# 菜品 CRUD API — dish5
# 来自 dish3/dish_online 的端点模式 + 正确 HTTPException 错误处理
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas import BaseResponse, PaginationResponse, PaginationParams
from ....schemas.dish import DishCreate, DishUpdate, DishResponse
from ....crud import crud_dish

router = APIRouter()

# 排序白名单 — 来自 dish3 的安全模式
ALLOWED_SORT_FIELDS = {
    "id", "name", "dtype", "ftype", "eats",
    "start_month", "end_month", "cooking_time", "difficulty",
    "sort_order", "created_at", "updated_at",
}


@router.get("/{dish_id}", response_model=BaseResponse[DishResponse])
async def get_dish(dish_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个菜品"""
    dish = await crud_dish.get(db, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail=f"菜品 #{dish_id} 不存在")
    return BaseResponse(data=dish)


@router.get("", response_model=PaginationResponse[DishResponse])
async def list_dishes(
    params: PaginationParams = Depends(),
    name: str = Query(None, description="菜名搜索"),
    dtype: str = Query(None, description="荤素类型筛选"),
    ftype: str = Query(None, description="主材类型筛选"),
    month: int = Query(None, description="应季月份筛选"),
    db: AsyncSession = Depends(get_db),
):
    """分页列表，支持搜索和筛选"""
    skip = (params.current - 1) * params.pageSize

    # 构建筛选条件
    filters = {}
    if name:
        filters["name"] = name
    if dtype:
        filters["dtype"] = dtype
    if ftype:
        filters["ftype"] = ftype

    items, total = await crud_dish.get_multi(
        db,
        skip=skip,
        limit=params.pageSize,
        sort_field=params.sort_field if params.sort_field in ALLOWED_SORT_FIELDS else None,
        sort_order=params.sort_order or "desc",
        allowed_sort_fields=ALLOWED_SORT_FIELDS,
        filters=filters,
    )

    # month 单独处理（因为它是范围查询，不适用 equal/like）
    if month is not None:
        from sqlalchemy import select
        from ....models.dish import Dish as DishModel
        items = [d for d in items if d.start_month <= month <= d.end_month]
        total = len(items)

    return PaginationResponse(
        data=items,
        total=total,
        current=params.current,
        pageSize=params.pageSize,
    )


@router.post("", response_model=BaseResponse[DishResponse])
async def create_dish(body: DishCreate, db: AsyncSession = Depends(get_db)):
    """创建菜品"""
    data = body.model_dump()

    # 转换枚举字符串为枚举值
    from ....models.dish import DtypeEnum, FtypeEnum, DifficultyEnum
    try:
        data["dtype"] = DtypeEnum(data["dtype"])
        data["ftype"] = FtypeEnum(data["ftype"])
        data["difficulty"] = DifficultyEnum(data.get("difficulty", "中等"))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"枚举值无效: {e}")

    # 转换子模型为 dict
    for field_name in [
        "main_ingredients", "side_ingredients", "seasonings",
        "cooking_steps", "attentions", "prep_steps",
    ]:
        if field_name in data and data[field_name]:
            data[field_name] = [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in data[field_name]
            ]

    dish = await crud_dish.create(db, obj_in=data)
    return BaseResponse(data=dish)


@router.patch("/{dish_id}", response_model=BaseResponse[DishResponse])
async def update_dish(
    dish_id: int, body: DishUpdate, db: AsyncSession = Depends(get_db)
):
    """部分更新菜品"""
    dish = await crud_dish.get(db, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail=f"菜品 #{dish_id} 不存在")

    update_data = body.model_dump(exclude_unset=True)

    # 转换枚举
    from ....models.dish import DtypeEnum, FtypeEnum, DifficultyEnum
    if "dtype" in update_data and update_data["dtype"]:
        try:
            update_data["dtype"] = DtypeEnum(update_data["dtype"])
        except ValueError:
            raise HTTPException(status_code=422, detail="无效的 dtype 值")
    if "ftype" in update_data and update_data["ftype"]:
        try:
            update_data["ftype"] = FtypeEnum(update_data["ftype"])
        except ValueError:
            raise HTTPException(status_code=422, detail="无效的 ftype 值")
    if "difficulty" in update_data and update_data["difficulty"]:
        try:
            update_data["difficulty"] = DifficultyEnum(update_data["difficulty"])
        except ValueError:
            raise HTTPException(status_code=422, detail="无效的 difficulty 值")

    # 转换 JSON 字段
    for field_name in [
        "main_ingredients", "side_ingredients", "seasonings",
        "cooking_steps", "attentions", "prep_steps",
    ]:
        if field_name in update_data and update_data[field_name] is not None:
            update_data[field_name] = [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in update_data[field_name]
            ]

    dish = await crud_dish.update(db, db_obj=dish, obj_in=update_data)
    return BaseResponse(data=dish)


@router.delete("/{dish_id}", response_model=BaseResponse)
async def delete_dish(dish_id: int, db: AsyncSession = Depends(get_db)):
    """删除单个菜品"""
    success = await crud_dish.delete(db, id=dish_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"菜品 #{dish_id} 不存在")
    return BaseResponse(detail="删除成功")


@router.delete("", response_model=BaseResponse)
async def batch_delete_dishes(
    ids: List[int], db: AsyncSession = Depends(get_db)
):
    """批量删除菜品 — 来自 dish3"""
    if len(ids) > 100:
        raise HTTPException(status_code=422, detail="单次最多删除100条")
    count = await crud_dish.delete_batch(db, ids=ids)
    return BaseResponse(detail=f"成功删除 {count} 条记录")


@router.get("/by-ingredient", response_model=BaseResponse)
async def find_by_ingredient(
    name: str = Query(..., description="食材名"), db: AsyncSession = Depends(get_db)
):
    """反向搜索：找出用到指定食材的所有菜品"""
    dishes = await crud_dish.find_by_ingredient(db, [name])
    return BaseResponse(data=dishes)
