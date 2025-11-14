from sqlalchemy import Column, String, Table

from config import database, metadata

from .model import MenuRoleBody

""" 菜单与角色对应关系表 - 功能CRUD模块 """
""" 模型映射 """
menuRole = Table(
    "menu_role",
    metadata,
    Column("menu_id", String, primary_key=True),
    Column("role_id", String, primary_key=True),
)

""" 根据主键进行删除 """


async def delete(role_id: str):
    try:
        await database.execute(menuRole.delete().where(menuRole.c.role_id == role_id))
        return True
    except Exception:
        return False


""" 添加 """


async def add(_menuRole: MenuRoleBody):
    values = _menuRole.dict()
    try:
        await database.execute(menuRole.insert().values(values))
        return True
    except Exception:
        return False
