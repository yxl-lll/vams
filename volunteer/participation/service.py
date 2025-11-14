import logging
import uuid
from datetime import datetime

from sqlalchemy import DATETIME, Column, Float, Integer, String, Table, func, select

from config import database, metadata
from utils.fix_query import FixQuery

from .model import ParticipationBody, ParticipationQuery, ParticipationUpdateBody

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

""" 活动参与记录 - 功能CRUD模块 """
""" 模型映射 """
participation = Table(
    "participation",
    metadata,
    Column("id", String, primary_key=True),
    Column("activity_id", String),
    Column("activity_name", String),
    Column("activity_image", String, nullable=True),
    Column("activity_type", String),
    Column("activity_date", DATETIME),
    Column("service_hours", Float),
    Column("participant_count", Integer),
    Column("check_in_time", DATETIME, nullable=True),
    Column("check_out_time", DATETIME, nullable=True),
    Column("status", String, default="registered"),
    Column("remark", String, nullable=True),
    Column("user_id", String),
    Column("user_name", String),
    Column("created_at", DATETIME),
    Column("updated_at", DATETIME),
    extend_existing=True,
)

""" 分页查询 """


async def page_data(
    start: int = 1, limit: int = 10, query_participation: ParticipationQuery = None
):
    try:
        logger.info(f"查询活动参与记录，页码：{start}，每页：{limit}")

        base_query = select(participation)
        total_query = select(func.count(participation.c.id)).select_from(participation)

        if query_participation:
            total_query, base_query = FixQuery.query(
                query_participation,
                val=query_participation,
                instance=participation,
                total_query=total_query,
                query=base_query,
            )

        list_data = await database.fetch_all(
            base_query.offset((start - 1) * limit).limit(limit)
        )
        total_result = await database.fetch_one(total_query)

        total_count = total_result.count_1 if total_result else 0
        logger.info(f"查询成功，总数：{total_count}，返回数据：{len(list_data)}")

        return total_count, list_data
    except Exception as e:
        logger.error(f"查询活动参与记录失败：{str(e)}", exc_info=True)
        return 0, []


""" 列表查询 """


async def list_data(query_participation: ParticipationQuery = None):
    try:
        logger.info("查询活动参与记录列表")

        base_query = select(participation)

        if query_participation:
            _, base_query = FixQuery.query(
                query_participation,
                val=query_participation,
                instance=participation,
                total_query=select(func.count(participation.c.id)),
                query=base_query,
            )

        list_data = await database.fetch_all(base_query)
        logger.info(f"查询成功，返回数据：{len(list_data)}")

        return list_data
    except Exception as e:
        logger.error(f"查询活动参与记录列表失败：{str(e)}", exc_info=True)
        return []


""" 根据主键获取单条数据 """


async def one(id: str):
    try:
        return await database.fetch_one(
            participation.select().where(participation.c.id == id)
        )
    except Exception as e:
        logger.error(f"查询单个活动参与记录失败：{str(e)}", exc_info=True)
        return None


""" 添加 """


async def add(_participation: ParticipationBody, current_user: dict):
    try:
        logger.info(
            f"添加活动参与记录：活动ID={_participation.activity_id}，用户ID={current_user['user_id']}"
        )

        existing = await database.fetch_one(
            select(participation).where(
                (participation.c.activity_id == _participation.activity_id)
                & (participation.c.user_id == current_user["user_id"])
                & (participation.c.status != "cancelled")
            )
        )
        if existing:
            logger.warning(
                f"用户{current_user['user_id']}已报名活动{_participation.activity_id}"
            )
            return False

        values = _participation.dict()
        values["id"] = str(uuid.uuid4())
        values["user_id"] = current_user["user_id"]
        values["user_name"] = current_user.get("nick_name", "未知用户")
        values["status"] = "registered"
        values["created_at"] = datetime.now()
        values["updated_at"] = datetime.now()

        await database.execute(participation.insert().values(values))
        logger.info(f"添加活动参与记录成功：{values['id']}")
        return True
    except Exception as err:
        logger.error(f"添加活动参与记录失败：{str(err)}", exc_info=True)
        return False


""" 修改 """


async def update(id: str, _participation: ParticipationUpdateBody):
    try:
        logger.info(f"更新活动参与记录：{id}")

        values = _participation.dict(exclude_unset=True)
        values["updated_at"] = datetime.now()

        await database.execute(
            participation.update().where(participation.c.id == id).values(values)
        )
        logger.info(f"更新活动参与记录成功：{id}")
        return True
    except Exception as e:
        logger.error(f"更新活动参与记录失败：{str(e)}", exc_info=True)
        return False


""" 删除 """


async def delete(id: str):
    try:
        logger.info(f"删除活动参与记录：{id}")

        await database.execute(participation.delete().where(participation.c.id == id))
        logger.info(f"删除活动参与记录成功：{id}")
        return True
    except Exception as e:
        logger.error(f"删除活动参与记录失败：{str(e)}", exc_info=True)
        return False


""" 签到 """


async def check_in(id: str, check_in_time: str):
    try:
        logger.info(f"签到活动参与记录：{id}")

        record = await database.fetch_one(
            select(participation).where(
                (participation.c.id == id) & (participation.c.status == "registered")
            )
        )
        if not record:
            logger.warning(f"签到失败：记录{id}不存在或状态不是已报名")
            return False

        await database.execute(
            participation.update()
            .where(participation.c.id == id)
            .values(
                status="checked_in",
                check_in_time=datetime.fromisoformat(check_in_time),
                updated_at=datetime.now(),
            )
        )
        logger.info(f"签到活动参与记录成功：{id}")
        return True
    except Exception as e:
        logger.error(f"签到活动参与记录失败：{str(e)}", exc_info=True)
        return False


""" 签退 """


async def check_out(id: str, check_out_time: str, service_hours: float):
    try:
        logger.info(f"签退活动参与记录：{id}")

        record = await database.fetch_one(
            select(participation).where(
                (participation.c.id == id) & (participation.c.status == "checked_in")
            )
        )
        if not record:
            logger.warning(f"签退失败：记录{id}不存在或状态不是已签到")
            return False

        await database.execute(
            participation.update()
            .where(participation.c.id == id)
            .values(
                status="completed",
                check_out_time=datetime.fromisoformat(check_out_time),
                service_hours=service_hours,
                updated_at=datetime.now(),
            )
        )
        logger.info(f"签退活动参与记录成功：{id}")
        return True
    except Exception as e:
        logger.error(f"签退活动参与记录失败：{str(e)}", exc_info=True)
        return False


""" 取消报名 """


async def cancel_participation(id: str):
    try:
        logger.info(f"取消报名活动参与记录：{id}")

        record = await database.fetch_one(
            select(participation).where(
                (participation.c.id == id) & (participation.c.status == "registered")
            )
        )
        if not record:
            logger.warning(f"取消报名失败：记录{id}不存在或状态不是已报名")
            return False

        await database.execute(
            participation.update()
            .where(participation.c.id == id)
            .values(status="cancelled", updated_at=datetime.now())
        )
        logger.info(f"取消报名活动参与记录成功：{id}")
        return True
    except Exception as e:
        logger.error(f"取消报名活动参与记录失败：{str(e)}", exc_info=True)
        return False


""" 获取用户统计数据 """


async def get_user_statistics(user_id: str):
    try:
        logger.info(f"获取用户统计数据：{user_id}")

        total_activities = await database.fetch_val(
            select(func.count(participation.c.id)).where(
                participation.c.user_id == user_id
            )
        )

        total_hours = await database.fetch_val(
            select(func.coalesce(func.sum(participation.c.service_hours), 0)).where(
                participation.c.user_id == user_id
            )
        )

        completed_activities = await database.fetch_val(
            select(func.count(participation.c.id)).where(
                (participation.c.user_id == user_id)
                & (participation.c.status == "completed")
            )
        )

        ongoing_activities = await database.fetch_val(
            select(func.count(participation.c.id)).where(
                (participation.c.user_id == user_id)
                & (participation.c.status == "checked_in")
            )
        )

        return {
            "total_activities": total_activities,
            "total_hours": round(float(total_hours), 1),
            "completed_activities": completed_activities,
            "ongoing_activities": ongoing_activities,
        }
    except Exception as e:
        logger.error(f"获取用户统计数据失败：{str(e)}", exc_info=True)
        return {
            "total_activities": 0,
            "total_hours": 0.0,
            "completed_activities": 0,
            "ongoing_activities": 0,
        }
