# 每日推荐记录模型 — dish5
# 基于 dish4 的 DailyRecommend，增加了 aggregated 预计算字段和通知追踪
from datetime import date, datetime

from sqlalchemy import Column, Integer, Date, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class DailyRecommend(Base):
    __tablename__ = "daily_recommends"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    date = Column(Date, unique=True, nullable=False, index=True, comment="推荐日期")

    # 推荐的菜品快照: [{"id": 1, "name": "红烧肉", "dtype": "硬菜"}, ...]
    recipes = Column(JSONB, default=list, comment="推荐菜品列表")

    # 购物清单: [{"name": "五花肉", "amount": "500g", "bought": false}, ...]
    shopping_list = Column(JSONB, default=list, comment="购物清单（含购买状态）")

    # 预计算的聚合数据（避免每次请求前端重复计算）
    # {"main_ingredients": [...], "side_ingredients": [...], "seasonings": [...],
    #  "cooking_steps": [...], "attentions": [...], "prep": {"wash": [...], "cut": [...], "marinate": [...]}}
    aggregated = Column(JSONB, default=dict, comment="聚合食材/步骤数据")

    # 通知状态
    notified = Column(Boolean, default=False, comment="是否已推送通知")
    notified_at = Column(DateTime, nullable=True, comment="推送时间")

    created_at = Column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return f"<DailyRecommend(id={self.id}, date={self.date})>"
