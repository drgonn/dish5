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
async def generate_recommend(
    target_date: date = None, db: AsyncSession = Depends(get_db)
):
    """手动生成每日推荐"""
    if target_date is None:
        target_date = date.today()

    service = RecommendService(db)
    recommend = await service.generate_daily_menu(target_date)
    return BaseResponse(data=recommend, detail="推荐生成成功")


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
