# 菜品-食材关系表 — dish5
# JSONB 的索引副本，仅用于搜索/匹配，不替代 dishes JSONB
from sqlalchemy import Column, Integer, String, ForeignKey, Index

from .base import Base


class DishIngredient(Base):
    __tablename__ = "dish_ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dish_id = Column(
        Integer, ForeignKey("dishes.id", ondelete="CASCADE"),
        nullable=False, index=True, comment="菜品ID"
    )
    name = Column(String(100), nullable=False, comment="标准化食材名")
    type = Column(String(20), default="main", comment="main/side/seasoning")

    __table_args__ = (
        Index("idx_di_name", "name"),
        Index("idx_di_dish_type", "dish_id", "type"),
    )
