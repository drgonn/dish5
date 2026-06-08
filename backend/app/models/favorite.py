# 收藏模型 — dish5
# 基于 dish4 的 Favorite 模型
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint

from .base import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    dish_id = Column(
        Integer,
        ForeignKey("dishes.id"),
        nullable=False,
        index=True,
        comment="菜品ID"
    )
    created_at = Column(DateTime, default=datetime.now, comment="收藏时间")

    __table_args__ = (
        UniqueConstraint("user_id", "dish_id", name="uq_user_dish"),
    )

    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, dish_id={self.dish_id})>"
