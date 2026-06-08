# 推荐偏好 API — dish5
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas import BaseResponse
from ....schemas.preference import PreferenceUpdate, PreferenceResponse
from ....crud import crud_preference

router = APIRouter()
DEFAULT_USER_ID = 1


@router.get("", response_model=BaseResponse[PreferenceResponse])
async def get_preferences(db: AsyncSession = Depends(get_db)):
    """获取推荐偏好"""
    pref = await crud_preference.get_or_create(db, DEFAULT_USER_ID)
    return BaseResponse(data=pref)


@router.put("", response_model=BaseResponse[PreferenceResponse])
async def update_preferences(
    body: PreferenceUpdate, db: AsyncSession = Depends(get_db)
):
    """更新推荐偏好（荤菜/素菜/汤数量）"""
    pref = await crud_preference.get_or_create(db, DEFAULT_USER_ID)
    pref = await crud_preference.update(db, db_obj=pref, obj_in=body.model_dump())
    return BaseResponse(data=pref, detail="偏好已更新")
