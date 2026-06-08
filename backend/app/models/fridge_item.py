# 冰箱库存 — dish5
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint

from .base import Base


class FridgeItem(Base):
    __tablename__ = "fridge_items"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = Column(Integer, default=1, nullable=False, index=True, comment="用户ID（预留）")
    ingredient_name = Column(String(100), nullable=False, comment="标准化食材名")
    category = Column(String(20), default="其他", comment="品类")
    quantity = Column(String(50), default="", comment="数量描述")
    added_from = Column(String(50), default="manual", comment="来源: manual/shopping/recommend_deduct")
    created_at = Column(DateTime, default=datetime.now, comment="入库时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    __table_args__ = (
        UniqueConstraint("user_id", "ingredient_name", name="uq_fridge_item"),
    )
