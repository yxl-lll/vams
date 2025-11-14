from datetime import datetime
from pydantic import BaseModel
from typing import Optional

""" 活动类型管理 - 模块模型定义 """


class ActivityTypeQuery(BaseModel):
    type_name: Optional[str] = None
    difficulty_level: Optional[str] = None


class ActivityTypeBody(BaseModel):
    type_name: str
    description: Optional[str] = None
    difficulty_level: str = 'normal'
    required_skills: Optional[str] = None
    remark: Optional[str] = None


class ActivityTypeUpdateBody(BaseModel):
    type_name: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    required_skills: Optional[str] = None
    remark: Optional[str] = None
