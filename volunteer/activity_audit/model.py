from datetime import datetime
from pydantic import BaseModel
from typing import Optional

""" 活动审核管理 - 模块模型定义 """

class ActivityAuditQuery(BaseModel):
    activity_id: Optional[str] = None
    auditor_id: Optional[str] = None
    audit_status: Optional[str] = None

class ActivityAuditBody(BaseModel):
    activity_id: str
    activity_name: str
    activity_type: str
    organizer_name: str
    organizer_phone: Optional[str] = None
    activity_location: str
    start_time: datetime
    end_time: datetime
    expected_participants: int
    activity_description: Optional[str] = None
    audit_status: str
    audit_opinion: Optional[str] = None

class ActivityAuditUpdateBody(BaseModel):
    audit_status: Optional[str] = None
    audit_opinion: Optional[str] = None

class ActivityAuditStatusUpdate(BaseModel):
    status: str
    opinion: Optional[str] = None
