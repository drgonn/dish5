# 每日推荐 API — dish5
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas import BaseResponse, PaginationResponse
from ....schemas.daily import DailyResponse, ShoppingUpdate
from ....crud import crud_daily
from ....services.recommend import RecommendService

router = APIRouter()


async def _notify_async(recommend):
    """后台发送通知，独立 db session"""
    try:
        from ....services.notification import send_notification
        await send_notification(recommend)
    except Exception:
        pass


@router.get("/today", response_model=BaseResponse[DailyResponse])
async def get_today_recommend(db: AsyncSession = Depends(get_db)):
    """获取今日推荐"""
    today = date.today()
    recommend = await crud_daily.get_by_date(db, today)
    if not recommend:
        return BaseResponse(detail="今日推荐尚未生成", data=None)
    return BaseResponse(data=recommend)


@router.get("/{target_date}", response_model=BaseResponse[DailyResponse])
async def get_date_recommend(
    target_date: date, db: AsyncSession = Depends(get_db)
):
    """获取指定日期的推荐"""
    recommend = await crud_daily.get_by_date(db, target_date)
    if not recommend:
        return BaseResponse(detail=f"{target_date} 的推荐不存在", data=None)
    return BaseResponse(data=recommend)


@router.post("/generate", response_model=BaseResponse[DailyResponse])
@router.get("/generate", response_model=BaseResponse[DailyResponse])
async def generate_recommend(
    target_date: date = None, db: AsyncSession = Depends(get_db)
):
    """手动生成每日推荐"""
    if target_date is None:
        target_date = date.today()

    service = RecommendService(db)
    recommend = await service.generate_daily_menu(target_date)

    # 后台发送通知，不阻塞响应
    import asyncio
    asyncio.create_task(_notify_async(recommend))

    return BaseResponse(data=recommend, detail="推荐生成成功")


@router.post("/today/swap/{recipe_id}", response_model=BaseResponse[DailyResponse])
async def swap_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """替换今日推荐中的单个菜品"""
    from ....models.dish import Dish
    from sqlalchemy import select

    today = date.today()
    recommend = await crud_daily.get_by_date(db, today)
    if not recommend:
        raise HTTPException(status_code=404, detail="今日推荐尚未生成")

    recipes = list(recommend.recipes or [])
    target = next((r for r in recipes if r.get("id") == recipe_id), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"菜品 #{recipe_id} 不在今日推荐中")

    target_dtype = target.get("dtype")
    used_ids = {r["id"] for r in recipes}

    # 找同类型、不同菜、最少吃过的
    result = await db.execute(
        select(Dish)
        .where(Dish.dtype == target_dtype, Dish.id.notin_(used_ids))
        .order_by(Dish.eats.asc())
        .limit(5)
    )
    candidates = result.scalars().all()
    if not candidates:
        raise HTTPException(status_code=404, detail="暂无可替换的同类型菜品")

    new_dish = candidates[0]

    # 替换
    for i, r in enumerate(recipes):
        if r["id"] == recipe_id:
            recipes[i] = {
                "id": new_dish.id,
                "name": new_dish.name,
                "dtype": new_dish.dtype.value if hasattr(new_dish.dtype, "value") else str(new_dish.dtype),
            }
            break

    # 重新加载完整 dish 对象来重新生成购物清单和聚合
    dish_ids = [r["id"] for r in recipes]
    result = await db.execute(select(Dish).where(Dish.id.in_(dish_ids)))
    all_dishes = list(result.scalars().all())

    service = RecommendService(db)
    shopping_list = service._generate_shopping_list(all_dishes)
    aggregated = service._aggregate_dishes(all_dishes)

    # 更新
    recommend = await crud_daily.create_or_update(
        db, target_date=today,
        recipes=recipes,
        shopping_list=shopping_list,
        aggregated=aggregated,
    )
    # 增加新菜 eats
    from ....crud import crud_dish
    await crud_dish.increment_eats(db, new_dish.id)

    return BaseResponse(data=recommend, detail=f"已替换为「{new_dish.name}」")


@router.get("/history/list", response_model=PaginationResponse[DailyResponse])
async def list_history(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """推荐历史列表"""
    from ....schemas import PaginationParams
    params = PaginationParams(current=page, pageSize=page_size)
    skip = (params.current - 1) * params.pageSize

    items, total = await crud_daily.get_multi(
        db,
        skip=skip,
        limit=params.pageSize,
        sort_field="date",
        sort_order="desc",
        allowed_sort_fields={"id", "date", "created_at"},
    )

    return PaginationResponse(
        data=items,
        total=total,
        current=params.current,
        pageSize=params.pageSize,
    )
