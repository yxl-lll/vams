import uuid
from datetime import datetime

from sqlalchemy import (DATE, DATETIME, Column, Integer, String, Table, func,
                        select)

from config import database, metadata
from system.user_role.model import UserRoleBody
from system.user_role.service import add as add_mr
from system.user_role.service import delete as del_by_user_id
from utils.fix_query import FixQuery
from utils.passwd import (get_password_hash, rsa_decrypt_password,
                          verify_password)

from .model import UpPwdBody, UserBody, UserQuery

""" 人员表 - 功能CRUD模块 """
""" 模型映射 """
user = Table(
    "user",
    metadata,
    Column("username", String),
    Column("id", String, primary_key=True),
    Column("created_at", DATETIME),
    Column("gender", Integer),
    Column("password", String),
    Column("status", Integer),
    Column("address", String),
    Column("avatar_url", String),
    Column("birthday", DATE),
    Column("email", String),
    Column("nick_name", String),
    Column("phone", String),
    Column("updated_at", DATETIME),
)

""" 分页查询 """


async def pages(page: int = 1, limit: int = 10, query_user: UserQuery = None):
    total_query, query = FixQuery.query(
        UserQuery,
        val=query_user,
        instance=user,
        total_query=select(func.count(user.c.id)).select_from(user),
        query=select(user),
    )
    list = await database.fetch_all(query.offset((page - 1) * limit).limit(limit))
    total = await database.fetch_one(total_query)
    return total.count_1, list


""" 根据主键进行删除 """


async def delete(id: str):
    try:
        await database.execute(user.delete().where(user.c.id == id))
        return True
    except Exception:
        return False


""" 添加 """


async def add(_user: UserBody):
    values = _user.dict()
    values["created_at"] = datetime.now()
    values["updated_at"] = datetime.now()
    values["id"] = str(uuid.uuid4())

    # 检查密码是否为空
    if not values.get("password"):
        print("错误：密码不能为空")
        return False

    values["password"] = get_password_hash(values["password"])

    # 处理角色ID - 支持字符串和列表格式
    role_ids = values.get("role_ids", "")
    if role_ids:
        if isinstance(role_ids, list):
            role_ids = role_ids
        elif isinstance(role_ids, str):
            role_ids = [id.strip() for id in role_ids.split(",") if id.strip()]
        else:
            role_ids = []
    else:
        role_ids = []

    del values["role_ids"]
    transaction = await database.transaction()
    try:
        await database.execute(user.insert().values(values))
        await del_by_user_id(values["id"])
        for role_id in role_ids:
            if role_id:  # 确保role_id不为空
                await add_mr(UserRoleBody(user_id=values["id"], role_id=role_id))
        await transaction.commit()
        return True
    except Exception as err:
        print(f"添加用户错误: {err}")
        await transaction.rollback()
        return False


""" 修改 """


async def update(id: str, _user: UserBody):
    values = _user.dict()
    values["updated_at"] = datetime.now()
    role_ids = values["role_ids"].split(",") if values["role_ids"] != None else []
    del values["role_ids"]
    if "password" in values:
        del values["password"]
    transaction = await database.transaction()
    try:
        await database.execute(user.update().where(user.c.id == id).values(values))
        await del_by_user_id(id)
        for role_id in role_ids:
            await add_mr(UserRoleBody(user_id=id, role_id=role_id))
        await transaction.commit()
        return True
    except Exception as err:
        print(err)
        await transaction.rollback()
        return False


""" 根据主键获取单条数据 """


async def one(id: str):
    return await database.fetch_one(user.select().where(user.c.id == id))


""" 根据 username 获取单条数据 """


async def username(username: str):
    return await database.fetch_one(user.select().where(user.c.username == username))


async def auth_role(user_id: str, role_ids):
    database.transaction().page()
    try:
        await del_by_user_id(user_id)
        for role_id in role_ids:
            await add_mr(UserRoleBody(role_id=role_id, user_id=user_id))
        database.transaction().commit()
        return True
    except Exception:
        database.transaction().rollback()
        return False


from utils.result import Result


async def upd_password(id: str, _user: UpPwdBody):
    values = _user.dict()
    user_val = await database.fetch_one(user.select().where(user.c.id == id))
    if verify_password(values["old_password"], user_val.password):
        password = get_password_hash(values["password"])
        await database.execute(
            f""" update user set password = '{password}' where id = '{id}'"""
        )
        return Result.fail(data="修改成功")
    return Result.fail(data="旧密码错误")
