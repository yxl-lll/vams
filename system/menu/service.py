
from sqlalchemy import select, Table, Column, Integer, String, DATETIME, DATE, func
from config import metadata, database
from datetime import datetime
from .model import Menu, MenuQuery, MenuBody
from utils.fix_query import FixQuery
import uuid
from system.menu_role.service import menuRole
from system.user_role.service import userRole
""" 菜单表 - 功能CRUD模块 """
""" 模型映射 """
menu = Table(
    "menu",
    metadata,
    Column("id", String, primary_key=True),
    Column("menu_name", String),
    Column("menu_status", Integer),
    Column("sort", Integer),
    Column("p_id", String),
    Column("auth_code", String),
    Column("icon", String),
    Column("type", Integer),
    Column("url", String),
    Column("updated_at", DATETIME),
    Column("created_at", DATETIME),
    Column("hurl", String)
)

""" 分页查询 """
async def pages(page: int = 1, limit: int = 10, query_menu: MenuQuery = None):
    total_query, query = FixQuery.query(MenuQuery,val=query_menu,instance=menu,total_query=select(func.count(menu.c.id)).select_from(menu),query=select(menu))
    list = await database.fetch_all(query.offset((page -1) * limit).limit(limit))
    total = await database.fetch_one(total_query)
    return total.count_1, list


async def lists(query_menu: MenuQuery = None):
    total_query, query = FixQuery.query(MenuQuery,val=query_menu,instance=menu,total_query=select(func.count(menu.c.id)).select_from(menu),query=select(menu))
    list = await database.fetch_all(query)
    return list

""" 根据主键进行删除 """
async def delete(id: str):
    try:
        await database.execute(menu.delete().where(menu.c.id == id))
        return True
    except Exception:
        return False

""" 添加 """
async def add(_menu: MenuBody):
    values = _menu.dict()
    values['created_at']=datetime.now()
    values['updated_at']=datetime.now()
    values['id'] = str(uuid.uuid4())
    try:
        await database.execute(menu.insert().values(values))
        return True
    except Exception:
        return False

""" 修改 """
async def update(id: str, _menu: MenuBody):
    values = _menu.dict()
    values['updated_at']=datetime.now()
    try:
        await database.execute(menu.update().where(menu.c.id == id).values(values))
        return True
    except Exception:
        return False

""" 根据主键获取单条数据 """
async def one(id: str):
    return await database.fetch_one(menu.select().where(menu.c.id == id))

async def get_menu(user_id: str):
    query = select(menu).join_from(
                menu, menuRole, menu.c.id == menuRole.c.menu_id
            ).join_from(
                menuRole,userRole,menuRole.c.role_id == userRole.c.role_id
            ).where(userRole.c.user_id == user_id).order_by(menu.c.sort.desc())
    return await database.fetch_all(query)
