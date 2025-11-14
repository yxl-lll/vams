
from sqlalchemy import Table, Column, String
from config import metadata, database
from datetime import datetime
from .model import UserRoleBody

""" 人员与角色中间表 - 功能CRUD模块 """
""" 模型映射 """
userRole = Table(
    "user_role",
    metadata,
    Column("role_id", String, primary_key=True),
    Column("user_id", String, primary_key=True)
)

async def lists(user_id: str):
    list = await database.fetch_all(userRole.select().where(userRole.c.user_id == user_id))
    return list


""" 根据主键进行删除 """
async def delete(user_id: str):
    try:
        await database.execute(userRole.delete().where(userRole.c.user_id == user_id))
        return True
    except Exception:
        return False

""" 添加 """
async def add(_userRole: UserRoleBody):
    values = _userRole.dict()
    try:
        await database.execute(userRole.insert().values(values))
        return True
    except Exception:
        return False