
from pydantic import BaseModel

""" 人员与角色中间表 - 模块模型定义 """
class UserRoleBody(BaseModel):
    role_id: str
    user_id: str
    