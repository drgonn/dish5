# 食材主表 — dish5
# 标准化食材名称 + 别名，用于冰箱匹配和搜索时名称统一
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    name = Column(String(100), unique=True, nullable=False, comment="标准化名称，如 土豆")
    category = Column(String(20), default="其他", comment="品类：肉禽蛋/蔬菜/豆制品/干货调料/水果/水产")
    aliases = Column(JSONB, default=list, comment='别名，如 ["土豆","马铃薯","洋芋"]')
    is_staple = Column(Boolean, default=False, comment="常用调料/常备品（购物清单中排除）")
