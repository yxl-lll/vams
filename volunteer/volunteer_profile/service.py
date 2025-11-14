import logging
import uuid
from datetime import date, datetime

from sqlalchemy import (
    DATE,
    DATETIME,
    DECIMAL,
    Column,
    Integer,
    String,
    Table,
    Text,
    func,
    select,
)

from config import database, metadata
from utils.fix_query import FixQuery

from .model import (
    VolunteerProfileBody,
    VolunteerProfileQuery,
    VolunteerProfileUpdateBody,
)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

""" 志愿者档案管理 - 功能CRUD模块 """
""" 模型映射 - 与数据库表结构保持一致 """
volunteer_profile = Table(
    "volunteer_profile",
    metadata,
    Column("id", String, primary_key=True),
    Column("user_id", String),
    Column("user_name", String),
    Column("real_name", String),
    Column("phone", String),
    Column("id_card", String),
    Column("gender", String),
    Column("birth_date", DATE),
    Column("total_service_hours", DECIMAL(8, 2)),  # 数据库中是decimal类型
    Column("total_activities", Integer),
    Column("skills", Text),
    Column("interests", Text),
    Column("volunteer_level", String),  # beginner, intermediate, advanced, expert
    Column("join_date", DATE),
    Column("status", Integer, default=1),
    Column("remarks", Text),  # 数据库中有这个字段
    Column("created_at", DATETIME),
    Column("updated_at", DATETIME),
)

""" 分页查询 """


async def page_data(
    start: int = 1,
    limit: int = 10,
    query_volunteer_profile: VolunteerProfileQuery = None,
):
    try:
        logger.info(f"查询志愿者档案，页码：{start}，每页：{limit}")

        # 基础查询
        base_query = select(volunteer_profile)
        total_query = select(func.count(volunteer_profile.c.id)).select_from(
            volunteer_profile
        )

        # 应用查询条件
        if query_volunteer_profile:
            total_query, base_query = FixQuery.query(
                query_volunteer_profile,
                val=query_volunteer_profile,
                instance=volunteer_profile,
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
        logger.error(f"查询志愿者档案失败：{str(e)}")
        return 0, []


""" 列表查询 """


async def list_data(query_volunteer_profile: VolunteerProfileQuery = None):
    try:
        logger.info("查询志愿者档案列表")

        # 基础查询
        base_query = select(volunteer_profile)
        total_query = select(func.count(volunteer_profile.c.id)).select_from(
            volunteer_profile
        )

        # 应用查询条件
        if query_volunteer_profile:
            total_query, base_query = FixQuery.query(
                query_volunteer_profile,
                val=query_volunteer_profile,
                instance=volunteer_profile,
                total_query=total_query,
                query=base_query,
            )

        # 执行查询
        list_data = await database.fetch_all(base_query)
        logger.info(f"查询成功，返回数据：{len(list_data)}")

        return list_data
    except Exception as e:
        logger.error(f"查询志愿者档案列表失败：{str(e)}")
        return []


""" 根据主键进行删除 """


async def delete(id: str):
    try:
        await database.execute(
            volunteer_profile.delete().where(volunteer_profile.c.id == id)
        )
        return True
    except Exception:
        return False


""" 添加志愿者档案 """


async def add(_volunteer_profile: VolunteerProfileBody):
    values = _volunteer_profile.dict()
    values["created_at"] = datetime.now()
    values["updated_at"] = datetime.now()
    values["id"] = str(uuid.uuid4())

    # 设置默认值
    if "total_service_hours" not in values:
        values["total_service_hours"] = 0
    if "total_activities" not in values:
        values["total_activities"] = 0

    # 处理service_hours字段（如果存在）
    if "service_hours" in values and values["service_hours"] is not None:
        values["total_service_hours"] = values.pop("service_hours")

    try:
        await database.execute(volunteer_profile.insert().values(values))
        return True
    except Exception as err:
        logger.error(f"添加志愿者档案失败: {str(err)}")
        return False


""" 修改志愿者档案 """


async def update(id: str, _volunteer_profile: VolunteerProfileUpdateBody):
    values = _volunteer_profile.dict(exclude_unset=True)
    values["updated_at"] = datetime.now()
    try:
        await database.execute(
            volunteer_profile.update()
            .where(volunteer_profile.c.id == id)
            .values(values)
        )
        return True
    except Exception:
        return False


""" 根据主键获取单条数据 """


async def one(id: str):
    return await database.fetch_one(
        volunteer_profile.select().where(volunteer_profile.c.id == id)
    )


""" 根据用户ID获取档案 """


async def get_by_user_id(user_id: str):
    return await database.fetch_one(
        volunteer_profile.select().where(volunteer_profile.c.user_id == user_id)
    )


""" 更新服务统计 """


async def update_service_stats(user_id: str, service_hours: int, activity_count: int):
    try:
        await database.execute(
            volunteer_profile.update()
            .where(volunteer_profile.c.user_id == user_id)
            .values(
                {
                    "total_service_hours": volunteer_profile.c.total_service_hours
                    + service_hours,
                    "total_activities": volunteer_profile.c.total_activities
                    + activity_count,
                    "updated_at": datetime.now(),
                }
            )
        )
        return True
    except Exception:
        return False


""" 获取志愿者统计 """


async def get_volunteer_statistics():
    try:
        # 统计各等级志愿者数量
        level_query = select(
            volunteer_profile.c.volunteer_level,
            func.count(volunteer_profile.c.id).label("count"),
        ).group_by(volunteer_profile.c.volunteer_level)

        level_stats = await database.fetch_all(level_query)

        # 统计总服务时长
        total_hours_query = select(func.sum(volunteer_profile.c.total_service_hours))
        total_hours = await database.fetch_one(total_hours_query)

        # 统计总活动数
        total_activities_query = select(func.sum(volunteer_profile.c.total_activities))
        total_activities = await database.fetch_one(total_activities_query)

        return {
            "level_stats": level_stats,
            "total_hours": total_hours.sum_1 or 0,
            "total_activities": total_activities.sum_1 or 0,
        }
    except Exception as err:
        print(err)
        return {"level_stats": [], "total_hours": 0, "total_activities": 0}


""" 获取技能标签统计 """


async def get_skills_statistics():
    try:
        # 这里可以实现技能标签的统计分析
        # 由于技能字段是文本，需要特殊处理
        return {"message": "技能统计功能开发中..."}
    except Exception as err:
        print(err)
        return {"message": "技能统计失败"}
