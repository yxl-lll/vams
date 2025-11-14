from datetime import datetime
from typing import Optional

from pydantic import BaseModel

""" 通知消息管理 - 模块模型定义 """


class NotificationQuery(BaseModel):
    type: Optional[str] = None
    target_user_id: Optional[str] = None
    is_read: Optional[bool] = None
    priority: Optional[str] = None
    # 在这里添加了缺失的 title 字段
    title: Optional[str] = None


class NotificationBody(BaseModel):
    title: str
    content: str
    type: str = "system"
    target_user_id: Optional[str] = None
    priority: str = "normal"
    expire_time: Optional[datetime] = None


class NotificationUpdateBody(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[str] = None
    expire_time: Optional[datetime] = None
    is_read: Optional[bool] = None
