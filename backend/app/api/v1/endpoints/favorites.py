# 收藏 API — dish5
# 暂时不需要认证，使用默认 user_id=1
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas import BaseResponse
from ....crud import crud_favorite

router = APIRouter()

DEFAULT_USER_ID = 1  # Phase 2 替换为真实认证用户


@router.get("", response_model=BaseResponse)
async def get_favorites(db: AsyncSession = Depends(get_db)):
    """获取收藏列表"""
    favorites = await crud_favorite.get_user_favorites(db, DEFAULT_USER_ID)
    return BaseResponse(data=favorites)


@router.post("", response_model=BaseResponse)
async def add_favorite(dish_id: int, db: AsyncSession = Depends(get_db)):
    """添加收藏"""
    existing = await crud_favorite.get_user_favorite(db, DEFAULT_USER_ID, dish_id)
    if existing:
        return BaseResponse(detail="已收藏过该菜品")

    fav = await crud_favorite.create(
        db, obj_in={"user_id": DEFAULT_USER_ID, "dish_id": dish_id}
    )
    return BaseResponse(data=fav, detail="收藏成功")


@router.delete("/{dish_id}", response_model=BaseResponse)
async def remove_favorite(dish_id: int, db: AsyncSession = Depends(get_db)):
    """取消收藏"""
    existing = await crud_favorite.get_user_favorite(db, DEFAULT_USER_ID, dish_id)
    if not existing:
        raise HTTPException(status_code=404, detail="未收藏该菜品")

    success = await crud_favorite.delete(db, id=existing.id)
    return BaseResponse(detail="已取消收藏")


@router.get("/check/{dish_id}", response_model=BaseResponse)
async def check_favorite(dish_id: int, db: AsyncSession = Depends(get_db)):
    """检查是否已收藏"""
    fav = await crud_favorite.get_user_favorite(db, DEFAULT_USER_ID, dish_id)
    return BaseResponse(data={"favorited": fav is not None})
