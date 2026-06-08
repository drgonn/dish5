# 每日推荐 Pydantic schemas — dish5
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel


class ShoppingItem(BaseModel):
    """购物清单单项"""
    name: str
    amount: str
    bought: bool = False


class DailyResponse(BaseModel):
    """每日推荐响应"""
    id: int
    date: date
    recipes: List[dict] = []
    shopping_list: List[dict] = []
    aggregated: dict = {}
    notified: bool = False
    notified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ShoppingUpdate(BaseModel):
    """更新购物清单已购状态"""
    items: List[ShoppingItem]
