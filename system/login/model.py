from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

""" 登录模块模型定义 """


class LoginBody(BaseModel):
    username: str
    password: str


class RegisterBody(BaseModel):
    password: str
    username: str
    nickname: str
