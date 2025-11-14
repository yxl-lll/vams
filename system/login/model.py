
from datetime import datetime, date
from pydantic import BaseModel
from decimal import Decimal

""" 登录模块模型定义 """

class LoginBody(BaseModel):
    username: str
    password: str
    
class RegisterBody(BaseModel):
    password: str
    username: str
    nickname: str
    