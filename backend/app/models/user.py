# 用户模型 — dish5
# 预留，Phase 1 不启用认证。数据库表会创建但 API 不强制登录。
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    username = Column(String(63), unique=True, nullable=False, index=True, comment="用户名")
    email = Column(String(127), unique=True, nullable=True, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="密码哈希")
    nickname = Column(String(63), nullable=True, comment="昵称")
    avatar_url = Column(String(255), default="", comment="头像")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_admin = Column(Boolean, default=False, comment="是否管理员")

    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
