# 收藏 Pydantic schemas — dish5
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FavoriteCreate(BaseModel):
    """添加收藏"""
    user_id: int = Field(1, description="用户ID（暂时默认1）")
    dish_id: int = Field(..., description="菜品ID")


class FavoriteResponse(BaseModel):
    """收藏响应"""
    id: int
    user_id: int
    dish_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
