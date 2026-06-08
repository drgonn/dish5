# 菜品 Pydantic schemas — dish5
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ——— JSON 子模型 ———

class IngredientItem(BaseModel):
    """食材项"""
    name: str = Field(..., description="食材名称")
    amount: str = Field("", description="用量")


class CookingStep(BaseModel):
    """烹饪步骤"""
    name: str = Field(..., description="步骤名称")
    step: int = Field(..., description="步骤序号")


class AttentionItem(BaseModel):
    """注意事项"""
    name: str = Field(..., description="注意内容")
    type: str = Field("注意", description="类型")


class PrepStep(BaseModel):
    """备菜步骤"""
    act: str = Field(..., description="动作：洗/切/腌")
    name: str = Field(..., description="食材名称")
    shape: Optional[str] = Field(None, description="切后的形状")


# ——— 请求 Schema ———

class DishCreate(BaseModel):
    """创建菜品"""
    name: str = Field(..., min_length=1, max_length=100, description="菜名")
    dtype: str = Field(..., description="荤素类型")
    ftype: str = Field(..., description="主材类型")
    start_month: int = Field(..., ge=1, le=12, description="应季开始月")
    end_month: int = Field(..., ge=1, le=12, description="应季结束月")
    cooking_time: int = Field(30, ge=1, description="烹饪时间(分钟)")
    difficulty: str = Field("中等", description="难度")
    main_ingredients: List[IngredientItem] = Field(default_factory=list)
    side_ingredients: List[IngredientItem] = Field(default_factory=list)
    seasonings: List[IngredientItem] = Field(default_factory=list)
    cooking_steps: List[CookingStep] = Field(default_factory=list)
    attentions: List[AttentionItem] = Field(default_factory=list)
    prep_steps: List[PrepStep] = Field(default_factory=list)
    image_url: Optional[str] = Field("", description="图片URL")
    sort_order: int = Field(0, description="排序序号")


class DishUpdate(BaseModel):
    """更新菜品 — 所有字段可选"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    dtype: Optional[str] = None
    ftype: Optional[str] = None
    start_month: Optional[int] = Field(None, ge=1, le=12)
    end_month: Optional[int] = Field(None, ge=1, le=12)
    cooking_time: Optional[int] = Field(None, ge=1)
    difficulty: Optional[str] = None
    main_ingredients: Optional[List[IngredientItem]] = None
    side_ingredients: Optional[List[IngredientItem]] = None
    seasonings: Optional[List[IngredientItem]] = None
    cooking_steps: Optional[List[CookingStep]] = None
    attentions: Optional[List[AttentionItem]] = None
    prep_steps: Optional[List[PrepStep]] = None
    image_url: Optional[str] = None
    sort_order: Optional[int] = None


# ——— 响应 Schema ———

class DishResponse(BaseModel):
    """菜品响应"""
    id: int
    name: str
    dtype: str
    ftype: str
    start_month: int
    end_month: int
    eats: int
    main_ingredients: List[dict] = []
    side_ingredients: List[dict] = []
    seasonings: List[dict] = []
    cooking_steps: List[dict] = []
    attentions: List[dict] = []
    prep_steps: List[dict] = []
    cooking_time: int
    difficulty: str
    image_url: str
    sort_order: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
