# 冰箱图鉴 API — dish5 V2
# 预定义常见主材，点亮/熄灭切换，根据已点亮的主材生成推荐
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.database import get_db
from ....schemas import BaseResponse
from ....crud import crud_fridge, crud_dish
from ....services.recommend import RecommendService

router = APIRouter()
DEFAULT_USER_ID = 1

# 常见主材图鉴列表（按常见度排序）
CHECKLIST = [
    # (名称, 品类, emoji)
    ("五花肉",  "肉禽蛋", "🥩"),
    ("排骨",    "肉禽蛋", "🦴"),
    ("猪里脊",  "肉禽蛋", "🥩"),
    ("牛肉",    "肉禽蛋", "🐂"),
    ("牛腩",    "肉禽蛋", "🐂"),
    ("鸡腿",    "肉禽蛋", "🍗"),
    ("鸡翅",    "肉禽蛋", "🍗"),
    ("鸡胸肉",  "肉禽蛋", "🐔"),
    ("鸭肉",    "肉禽蛋", "🦆"),
    ("鸡蛋",    "肉禽蛋", "🥚"),
    ("虾",      "水产",   "🦐"),
    ("鱼",      "水产",   "🐟"),
    ("土豆",    "蔬菜",   "🥔"),
    ("番茄",    "蔬菜",   "🍅"),
    ("豆腐",    "豆制品", "🧈"),
    ("茄子",    "蔬菜",   "🍆"),
    ("青椒",    "蔬菜",   "🌶️"),
    ("豆角",    "蔬菜",   "🫘"),
    ("包菜",    "蔬菜",   "🥬"),
    ("西兰花",  "蔬菜",   "🥦"),
    ("黄瓜",    "蔬菜",   "🥒"),
    ("白菜",    "蔬菜",   "🥬"),
    ("萝卜",    "蔬菜",   "🥕"),
    ("韭菜",    "蔬菜",   "🌿"),
    ("蒜苗",    "蔬菜",   "🌱"),
    ("洋葱",    "蔬菜",   "🧅"),
    ("芹菜",    "蔬菜",   "🥬"),
    ("玉米",    "蔬菜",   "🌽"),
    ("冬瓜",    "蔬菜",   "🍈"),
    ("丝瓜",    "蔬菜",   "🥒"),
    ("生菜",    "蔬菜",   "🥬"),
]


@router.get("/checklist", response_model=BaseResponse)
async def get_checklist(db: AsyncSession = Depends(get_db)):
    """获取图鉴列表，标记哪些已点亮"""
    fridge_names = set(await crud_fridge.get_all_names(db, DEFAULT_USER_ID))
    result = []
    for name, category, emoji in CHECKLIST:
        result.append({
            "name": name,
            "category": category,
            "emoji": emoji,
            "lit": name in fridge_names,  # 已点亮
        })
    return BaseResponse(data=result)


@router.post("/toggle", response_model=BaseResponse)
async def toggle_item(
    ingredient_name: str, db: AsyncSession = Depends(get_db)
):
    """切换食材点亮/熄灭状态"""
    existing = await crud_fridge.get_by_name(db, DEFAULT_USER_ID, ingredient_name)
    if existing:
        await crud_fridge.remove_by_name(db, DEFAULT_USER_ID, ingredient_name)
        return BaseResponse(detail=f"「{ingredient_name}」已熄灭", data={"lit": False})
    else:
        await crud_fridge.add_or_update(
            db, user_id=DEFAULT_USER_ID,
            ingredient_name=ingredient_name,
        )
        return BaseResponse(detail=f"「{ingredient_name}」已点亮", data={"lit": True})


@router.post("/generate-recommend")
async def generate_from_fridge(
    meat_count: int = 1, vegetable_count: int = 2, soup_count: int = 1,
    db: AsyncSession = Depends(get_db),
):
    """根据冰箱已点亮的主材生成今日推荐"""
    from datetime import date

    fridge_names = await crud_fridge.get_all_names(db, DEFAULT_USER_ID)
    if not fridge_names:
        return {"code": 200, "success": True, "detail": "请先点亮至少一种食材", "data": None}
    service = RecommendService(db)
    today = date.today()
    recommend = await service.generate_daily_menu(
        today,
        meat_count=meat_count,
        vegetable_count=vegetable_count,
        soup_count=soup_count,
        must_include_ingredients=fridge_names,
    )
    # 转 dict 避免 Pydantic 序列化 DailyRecommend 失败
    return {
        "code": 200, "success": True,
        "detail": "已根据冰箱库存生成推荐",
        "data": {
            "id": recommend.id, "date": str(recommend.date),
            "recipes": recommend.recipes,
            "shopping_list": recommend.shopping_list,
            "aggregated": recommend.aggregated,
        },
    }
