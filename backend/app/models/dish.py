# 菜品/菜谱模型 — dish5
# 整合 dish3 的分类枚举和季节/计数字段 + dish_online 的丰富 JSON 字段 + dish4 的元数据字段
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class DtypeEnum(str, Enum):
    """荤素类型 — 来自 dish3 Mydish"""
    A = "硬菜"
    B = "肉汤"
    C = "素汤"
    D = "素菜"
    E = "半素"


class FtypeEnum(str, Enum):
    """主材类型 — 来自 dish3 Mydish"""
    A = "跑"    # 猪牛羊
    B = "飞"    # 鸡鸭鹅
    C = "游"    # 鱼虾海鲜
    D = "草"    # 素菜


class DifficultyEnum(str, Enum):
    """难度 — 来自 dish4"""
    SIMPLE = "简单"
    MEDIUM = "中等"
    HARD = "困难"


class Dish(Base):
    __tablename__ = "dishes"

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    # 基本信息
    name = Column(String(100), unique=True, nullable=False, comment="菜名")

    # 分类 — 来自 dish3
    dtype = Column(SQLEnum(DtypeEnum), nullable=False, comment="荤素类型")
    ftype = Column(SQLEnum(FtypeEnum), nullable=False, comment="主材类型")

    # 季节性 — 来自 dish3
    start_month = Column(SmallInteger, nullable=False, comment="应季开始月(1-12)")
    end_month = Column(SmallInteger, nullable=False, comment="应季结束月(1-12)")

    # 推荐计数 — 来自 dish3
    eats = Column(Integer, default=0, comment="被推荐次数")

    # JSON 字段 — 来自 dish_online，重命名更清晰
    # [{"name": "五花肉", "amount": "500g"}, ...]
    main_ingredients = Column(JSONB, default=list, comment="主料")
    # [{"name": "葱", "amount": "2根"}, ...]
    side_ingredients = Column(JSONB, default=list, comment="辅料")
    # [{"name": "生抽", "amount": "2勺"}, ...]
    seasonings = Column(JSONB, default=list, comment="调料")
    # [{"name": "焯水", "step": 1}, ...]
    cooking_steps = Column(JSONB, default=list, comment="烹饪步骤")
    # [{"name": "小火慢炖", "type": "注意"}, ...]
    attentions = Column(JSONB, default=list, comment="注意事项")
    # [{"act": "洗", "name": "五花肉"}, {"act": "切", "name": "五花肉切块"}, ...]
    prep_steps = Column(JSONB, default=list, comment="备菜步骤")

    # 元数据 — 来自 dish4
    cooking_time = Column(Integer, default=30, comment="烹饪时间(分钟)")
    difficulty = Column(
        SQLEnum(DifficultyEnum),
        default=DifficultyEnum.MEDIUM,
        comment="难度"
    )
    image_url = Column(String(255), default="", comment="图片URL")
    sort_order = Column(Integer, default=0, comment="排序序号")

    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

    def __repr__(self):
        return f"<Dish(id={self.id}, name='{self.name}', dtype={self.dtype})>"
