from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

""" 志愿者档案管理 - 模块模型定义 """


class VolunteerProfileQuery(BaseModel):
    user_name: Optional[str] = None
    volunteer_level: Optional[str] = None
    skills: Optional[str] = None


class VolunteerProfileBody(BaseModel):
    user_id: str
    user_name: str
    real_name: Optional[str] = None
    phone: Optional[str] = None
    id_card: Optional[str] = None
    gender: Optional[str] = "男"
    birth_date: Optional[date] = None
    skills: Optional[str] = None
    interests: Optional[str] = None
    volunteer_level: str = "bronze"
    join_date: Optional[date] = None
    status: Optional[int] = 1
    remarks: Optional[str] = None


class VolunteerProfileUpdateBody(BaseModel):
    real_name: Optional[str] = None
    phone: Optional[str] = None
    id_card: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    skills: Optional[str] = None
    interests: Optional[str] = None
    volunteer_level: Optional[str] = None
    join_date: Optional[date] = None
    status: Optional[int] = None
    remarks: Optional[str] = None
