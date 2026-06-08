from fastapi import APIRouter
from .endpoints import dishes, daily, shopping, favorites, aggregation, fridge, preferences

api_router = APIRouter()

api_router.include_router(dishes.router, prefix="/dishes", tags=["菜品管理"])
api_router.include_router(daily.router, prefix="/daily", tags=["每日推荐"])
api_router.include_router(shopping.router, prefix="/shopping", tags=["购物清单"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["收藏管理"])
api_router.include_router(aggregation.router, prefix="", tags=["聚合"])
api_router.include_router(fridge.router, prefix="/fridge", tags=["冰箱库存"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["推荐偏好"])
