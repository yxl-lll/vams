
from datetime import datetime, date
from pydantic import BaseModel
from decimal import Decimal

""" 人员表 - 模块模型定义 """
class User(BaseModel):
    username: str
    id: str
    created_at: datetime
    gender: int
    password: str | None = None
    status: int | None = None
    address: str | None = None
    avatar_url: str | None = None
    birthday: date | None = None
    email: str | None = None
    nick_name: str | None = None
    phone: str | None = None
    updated_at: datetime | None = None

class UserQuery(BaseModel):
    username: str | None = None
    gender: int | None = None
    password: str | None = None
    status: int | None = None
    address: str | None = None
    avatar_url: str | None = None
    birthday: date | None = None
    email: str | None = None
    nick_name: str | None = None
    phone: str | None = None

class UserBody(BaseModel):
    username: str
    password: str | None = None
    status: int | None = None
    gender: int | None = None
    address: str | None = None
    avatar_url: str | None = None
    birthday: date | None = None
    email: str | None = None
    nick_name: str | None = None
    phone: str | None = None
    role_ids: str | None = None

class UpPwdBody(BaseModel):
    password: str | None = None
    repassword: str | None = None
    old_password: str | None = None
    