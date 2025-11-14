
from datetime import datetime, date
from pydantic import BaseModel
from decimal import Decimal

""" 角色表 - 模块模型定义 """
class Role(BaseModel):
    id: str
    created_at: datetime
    role_name: str
    role_desc: str | None = None
    updated_at: datetime | None = None

class RoleQuery(BaseModel):
    role_name: str | None = None
    role_desc: str | None = None

class RoleBody(BaseModel):
    role_name: str
    role_desc: str | None = None
    menu_ids: str
    