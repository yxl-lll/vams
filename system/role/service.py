import uuid
from datetime import datetime

from sqlalchemy import (DATE, DATETIME, Column, Integer, String, Table, func,
                        select)

from config import database, metadata
from system.menu.model import MenuQuery
from system.menu.service import lists as list_menu
from system.menu.service import menu
from system.menu_role.model import MenuRoleBody
from system.menu_role.service import add as add_mr
from system.menu_role.service import delete as del_by_role_id
from system.menu_role.service import menuRole
from system.user_role.service import userRole
from utils.fix_query import FixQuery

from .model import RoleBody, RoleQuery

""" 角色表 - 功能CRUD模块 """
""" 模型映射 """
role = Table(
    "role",
    metadata,
    Column("id", String, primary_key=True),
    Column("created_at", DATETIME),
    Column("role_name", String),
    Column("role_desc", String),
    Column("updated_at", DATETIME),
)

""" 分页查询 """


async def pages(page: int = 1, limit: int = 10, query_role: RoleQuery = None):
    total_query, query = FixQuery.query(
        RoleQuery,
        val=query_role,
        instance=role,
        total_query=select(func.count(role.c.id)).select_from(role),
        query=select(role),
    )
    list = await database.fetch_all(query.offset((page - 1) * limit).limit(limit))
    total = await database.fetch_one(total_query)
    return total.count_1, list


async def lists(query_role: RoleQuery = None):
    total_query, query = FixQuery.query(
        RoleQuery,
        val=query_role,
        instance=role,
        total_query=select(func.count(role.c.id)).select_from(role),
        query=select(role),
    )
    list = await database.fetch_all(query)
    return list


""" 根据主键进行删除 """


async def delete(id: str):
    try:
        await database.execute(role.delete().where(role.c.id == id))
        return True
    except Exception:
        return False


""" 添加 """


async def add(_role: RoleBody):
    values = _role.dict()
    values["created_at"] = datetime.now()
    values["updated_at"] = datetime.now()
    values["id"] = str(uuid.uuid4())
    menu_ids = values["menu_ids"].split(",")
    del values["menu_ids"]
    transaction = await database.transaction()
    try:
        await database.execute(role.insert().values(values))
        await del_by_role_id(values["id"])
        for menu_id in menu_ids:
            await add_mr(MenuRoleBody(role_id=values["id"], menu_id=menu_id))
        await transaction.commit()
        return True
    except Exception:
        await transaction.rollback()
        return False


""" 修改 """


async def update(id: str, _role: RoleBody):
    values = _role.dict()
    values["updated_at"] = datetime.now()
    menu_ids = values["menu_ids"].split(",")
    del values["menu_ids"]
    transaction = await database.transaction()
    try:
        await database.execute(role.update().where(role.c.id == id).values(values))
        await del_by_role_id(id)
        for menu_id in menu_ids:
            await add_mr(MenuRoleBody(role_id=id, menu_id=menu_id))
        await transaction.commit()
        return True
    except Exception as err:

        await transaction.rollback()
        return False


""" 根据主键获取单条数据 """


async def one(id: str):
    return await database.fetch_one(role.select().where(role.c.id == id))


async def authorize(role_id: str, menu_ids):
    transaction = await database.transaction()
    try:
        await del_by_role_id(role_id)
        for menu_id in menu_ids:
            await add_mr(MenuRoleBody(role_id=role_id, menu_id=menu_id))
        await transaction.commit()
        return True
    except Exception:
        await transaction.rollback()
        return False


async def get_auth_menu(role_id: str):
    if role_id is not None and role_id != "":
        query = (
            select(menu.c.id)
            .join_from(menu, menuRole, menu.c.id == menuRole.c.menu_id)
            .where(menuRole.c.role_id == role_id)
        )
        return await list_menu(MenuQuery()), await database.fetch_all(query)
    return await list_menu(MenuQuery()), []


async def get_auth_role(user_id: str):
    if user_id is not None and user_id != "":
        return await lists(RoleQuery()), await database.fetch_all(
            select(userRole.c.role_id).where(userRole.c.user_id == user_id)
        )
    return await lists(RoleQuery()), []
