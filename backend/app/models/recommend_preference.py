# 推荐偏好 — dish5
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

from .base import Base


class RecommendPreference(Base):
    __tablename__ = "recommend_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = Column(Integer, default=1, unique=True, nullable=False, comment="用户ID（预留）")
    meat_count = Column(Integer, default=1, comment="荤菜数量")
    vegetable_count = Column(Integer, default=2, comment="素菜数量")
    soup_count = Column(Integer, default=1, comment="汤数量")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
