# 通用 Pydantic 响应模型 — dish5
# 来自 dish3 的 BaseResponse / PaginationResponse 模式，保留其好的设计
from typing import Optional, Generic, TypeVar, Literal

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """分页请求参数 — 来自 dish3"""
    current: int = Field(1, ge=1, description="当前页码")
    pageSize: int = Field(10, ge=1, le=1000, description="每页数量")
    sort_field: Optional[str] = Field(None, description="排序字段")
    sort_order: Optional[Literal["asc", "desc"]] = Field("desc", description="排序方式")


class PaginationResponse(BaseModel, Generic[T]):
    """分页响应 — 来自 dish3"""
    code: int = 200
    success: bool = True
    data: list[T]
    total: int
    current: int
    pageSize: int


class BaseResponse(BaseModel, Generic[T]):
    """通用响应 — 来自 dish3"""
    code: int = 200
    success: bool = True
    detail: Optional[str] = None
    showType: Optional[int] = None
    data: Optional[T] = None
