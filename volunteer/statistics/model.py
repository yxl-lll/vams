from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional

""" 统计报表 - 模块模型定义 """


class StatisticsQuery(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    activity_type: Optional[str] = None
    user_id: Optional[str] = None


class VolunteerStatistics(BaseModel):
    total_volunteers: int
    total_activities: int
    total_participations: int
    total_service_hours: float
    completed_activities: int
    ongoing_activities: int


class ActivityStatistics(BaseModel):
    activity_type: str
    count: int
    total_participants: int
    total_service_hours: float


class UserStatistics(BaseModel):
    user_id: str
    user_name: str
    total_activities: int
    total_service_hours: float
    volunteer_level: str
