# 推荐偏好 Pydantic schemas — dish5
from pydantic import BaseModel, Field


class PreferenceUpdate(BaseModel):
    meat_count: int = Field(1, ge=0, le=10, description="荤菜数量")
    vegetable_count: int = Field(2, ge=0, le=10, description="素菜数量")
    soup_count: int = Field(1, ge=0, le=10, description="汤数量")
    prefer_healthy: bool = Field(False, description="偏好健康")


class PreferenceResponse(BaseModel):
    id: int
    user_id: int
    meat_count: int
    vegetable_count: int
    soup_count: int
    prefer_healthy: bool = False

    class Config:
        from_attributes = True
