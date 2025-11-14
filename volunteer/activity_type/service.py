import logging
import uuid
from datetime import datetime

from sqlalchemy import DATETIME, Column, Integer, String, Table, Text, func, select

from config import database, metadata
from utils.fix_query import FixQuery

from .model import ActivityTypeBody, ActivityTypeQuery, ActivityTypeUpdateBody

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

""" 活动类型管理 - 功能CRUD模块 """
""" 模型映射 """
activity_type = Table(
    "activity_type",
    metadata,
    Column("id", String, primary_key=True),
    Column("type_name", String),
    Column("description", Text),
    Column("difficulty_level", String),
    Column("required_skills", Text),
    Column("remark", String),
    Column("created_at", DATETIME),
    Column("updated_at", DATETIME),
)

""" 分页查询 """


async def page_data(
    start: int = 1, limit: int = 10, query_activity_type: ActivityTypeQuery = None
):
    try:
        logger.info(f"查询活动类型，页码：{start}，每页：{limit}")

        # 基础查询
        base_query = select(activity_type)
        total_query = select(func.count(activity_type.c.id)).select_from(activity_type)

        # 应用查询条件
        if query_activity_type:
            total_query, base_query = FixQuery.query(
                query_activity_type,
                val=query_activity_type,
                instance=activity_type,
                total_query=total_query,
                query=base_query,
            )

        # 执行查询
        list_data = await database.fetch_all(
            base_query.offset((start - 1) * limit).limit(limit)
        )
        total_result = await database.fetch_one(total_query)

        total_count = total_result.count_1 if total_result else 0
        logger.info(f"查询成功，总数：{total_count}，返回数据：{len(list_data)}")

        return total_count, list_data
    except Exception as e:
        logger.error(f"查询活动类型失败：{str(e)}")
        return 0, []


""" 列表查询 """


async def list_data(query_activity_type: ActivityTypeQuery = None):
    try:
        logger.info("查询活动类型列表")

        # 基础查询
        base_query = select(activity_type)
        total_query = select(func.count(activity_type.c.id)).select_from(activity_type)

        # 应用查询条件
        if query_activity_type:
            total_query, base_query = FixQuery.query(
                query_activity_type,
                val=query_activity_type,
                instance=activity_type,
                total_query=total_query,
                query=base_query,
            )

        # 执行查询
        list_data = await database.fetch_all(base_query)
        logger.info(f"查询成功，返回数据：{len(list_data)}")

        return list_data
    except Exception as e:
        logger.error(f"查询活动类型列表失败：{str(e)}")
        return []


""" 根据主键进行删除 """


async def delete(id: str):
    try:
        await database.execute(activity_type.delete().where(activity_type.c.id == id))
        return True
    except Exception:
        return False


""" 添加 """


async def add(_activity_type: ActivityTypeBody):
    values = _activity_type.dict()
    values["created_at"] = datetime.now()
    values["updated_at"] = datetime.now()
    values["id"] = str(uuid.uuid4())
    try:
        await database.execute(activity_type.insert().values(values))
        return True
    except Exception as err:
        print(err)
        return False


""" 修改 """


async def update(id: str, _activity_type: ActivityTypeUpdateBody):
    values = _activity_type.dict(exclude_unset=True)
    values["updated_at"] = datetime.now()
    try:
        await database.execute(
            activity_type.update().where(activity_type.c.id == id).values(values)
        )
        return True
    except Exception:
        return False


""" 根据主键获取单条数据 """


async def one(id: str):
    return await database.fetch_one(
        activity_type.select().where(activity_type.c.id == id)
    )
