from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

""" 活动计划管理 - 模块模型定义 """


class VolunteerPlansQuery(BaseModel):
    activity_type: Optional[str] = None
    activity_name: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[str] = None
    creator_role: Optional[str] = None  # <--- 新增：用于查询过滤


class VolunteerPlansBody(BaseModel):
    activity_name: str
    activity_date: datetime
    activity_type: str
    location: str
    service_hours: Decimal
    max_participants: int
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    remark: Optional[str] = None


class VolunteerPlansUpdateBody(BaseModel):
    activity_name: Optional[str] = None
    activity_date: Optional[datetime] = None
    activity_type: Optional[str] = None
    location: Optional[str] = None
    service_hours: Optional[Decimal] = None
    max_participants: Optional[int] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    remark: Optional[str] = None
    status: Optional[str] = None
    creator_role: Optional[str] = None  # <--- 新增：虽然创建时设置，但更新模型也带上


class VolunteerPlansStatusUpdate(BaseModel):
    status: str  # <--- 补充完整，原文件可能遗漏
