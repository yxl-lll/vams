from datetime import datetime
from pydantic import BaseModel
from typing import Optional

""" 活动参与记录 - 模块模型定义 """

class ParticipationQuery(BaseModel):
    activity_name: Optional[str] = None
    status: Optional[str] = None

class ParticipationBody(BaseModel):
    activity_id: str
    activity_name: str
    activity_image: Optional[str] = None
    activity_type: str
    activity_date: datetime
    service_hours: float
    participant_count: int
    remark: Optional[str] = None

class ParticipationUpdateBody(BaseModel):
    participant_count: Optional[int] = None
    remark: Optional[str] = None

class CheckInBody(BaseModel):
    check_in_time: str

class CheckOutBody(BaseModel):
    check_out_time: str
    service_hours: float
