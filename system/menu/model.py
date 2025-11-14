
from datetime import datetime, date
from pydantic import BaseModel
from decimal import Decimal

""" 菜单表 - 模块模型定义 """
class Menu(BaseModel):
    id: str
    menu_name: str
    menu_status: int
    sort: int
    p_id: str | None = None
    auth_code: str | None = None
    created_at: datetime | None = None
    icon: str | None = None
    type: int | None = None
    updated_at: datetime | None = None
    url: str | None = None
    hurl: str | None = None

class MenuQuery(BaseModel):
    menu_name: str | None = None
    menu_status: int | None = None
    sort: int | None = None
    p_id: str | None = None
    auth_code: str | None = None
    icon: str | None = None
    type: int | None = None
    url: str | None = None
    hurl: str | None = None

class MenuBody(BaseModel):
    menu_name: str
    menu_status: int
    sort: int
    p_id: str | None = None
    auth_code: str | None = None
    icon: str | None = None
    type: int | None = None
    url: str | None = None
    hurl: str | None = None
    