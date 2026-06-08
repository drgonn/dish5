# 冰箱 Pydantic schemas — dish5
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class FridgeItemCreate(BaseModel):
    ingredient_name: str = Field(..., min_length=1, max_length=100)
    category: str = Field("其他")
    quantity: str = Field("")
    added_from: str = Field("manual")


class FridgeItemResponse(BaseModel):
    id: int
    user_id: int
    ingredient_name: str
    category: str
    quantity: str
    added_from: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ShoppingCheckResult(BaseModel):
    """购物清单与冰箱对比结果"""
    need_buy: list = []       # 需要买的
    already_have: list = []   # 冰箱已有


class FridgeMatchResult(BaseModel):
    """冰箱匹配结果"""
    dish_id: int
    dish_name: str
    dtype: str
    match_level: str          # "完全可做" / "差1样" / "差2样"
    missing: List[str] = []   # 缺少的食材


class FridgeBatchAdd(BaseModel):
    """从购物清单一键入库"""
    ingredient_names: List[str]
