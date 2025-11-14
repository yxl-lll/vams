import logging
import uuid
from datetime import datetime

from sqlalchemy import DATETIME, Column, Integer, String, Table, Text, func, select

from config import database, metadata
from utils.fix_query import FixQuery

from .model import ActivityAuditBody, ActivityAuditQuery, ActivityAuditUpdateBody

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

""" 活动审核管理 - 功能CRUD模块 """
""" 模型映射 - 与数据库表结构保持一致 """
activity_audit = Table(
    "activity_audit",
    metadata,
    Column("id", String, primary_key=True),
    Column("activity_id", String),
    Column("activity_name", String),
    Column("activity_type", String),
    Column("organizer_name", String),
    Column("organizer_phone", String),
    Column("activity_location", String),
    Column("start_time", DATETIME),
    Column("end_time", DATETIME),
    Column("expected_participants", Integer),
    Column("activity_description", Text),
    Column("auditor_id", String),
    Column("auditor_name", String),
    Column("audit_status", String),  # pending, approved, rejected
    Column("audit_remarks", Text),
    Column("audit_time", DATETIME),
    Column("created_at", DATETIME),
    Column("updated_at", DATETIME),
)

""" 分页查询 """


async def page_data(
    start: int = 1, limit: int = 10, query_activity_audit: ActivityAuditQuery = None
):
    try:
        logger.info(f"查询活动审核，页码：{start}，每页：{limit}")
        base_query = select(activity_audit)
        total_query = select(func.count(activity_audit.c.id)).select_from(
            activity_audit
        )
        if query_activity_audit:
            total_query, base_query = FixQuery.query(
                query_activity_audit,
                val=query_activity_audit,
                instance=activity_audit,
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
        logger.error(f"查询活动审核失败：{str(e)}")
        return 0, []


""" 列表查询 """


async def list_data(query_activity_audit: ActivityAuditQuery = None):
    try:
        logger.info("查询活动审核列表")
        base_query = select(activity_audit)
        if query_activity_audit:
            _, base_query = FixQuery.query(
                query_activity_audit,
                val=query_activity_audit,
                instance=activity_audit,
                total_query=select(func.count(activity_audit.c.id)),
                query=base_query,
            )
        list_data = await database.fetch_all(base_query)
        logger.info(f"查询成功，返回数据：{len(list_data)}")
        return list_data
    except Exception as e:
        logger.error(f"查询活动审核列表失败：{str(e)}")
        return []


""" 根据主键进行删除 """


async def delete(id: str):
    try:
        await database.execute(activity_audit.delete().where(activity_audit.c.id == id))
        return True
    except Exception:
        return False


""" 添加审核记录 """


async def add(_activity_audit: ActivityAuditBody, auditor_info: any):
    values = _activity_audit.dict()
    values["id"] = str(uuid.uuid4())
    values["created_at"] = datetime.now()
    values["updated_at"] = datetime.now()
    values["auditor_id"] = None
    values["auditor_name"] = None
    values["audit_time"] = None
    if "audit_opinion" in values:
        values["audit_remarks"] = values.pop("audit_opinion")
    try:
        await database.execute(activity_audit.insert().values(values))
        logger.info(f"审核记录创建成功 for activity_id: {values['activity_id']}")
        return True
    except Exception as err:
        logger.error(f"添加审核记录失败：{str(err)}", exc_info=True)
        return False


""" 修改审核记录 """


async def update(id: str, _activity_audit: ActivityAuditUpdateBody):
    values = _activity_audit.dict(exclude_unset=True)
    values["updated_at"] = datetime.now()
    if "audit_opinion" in values:
        values["audit_remarks"] = values.pop("audit_opinion")
    try:
        await database.execute(
            activity_audit.update().where(activity_audit.c.id == id).values(values)
        )
        return True
    except Exception:
        return False


""" 根据主键获取单条数据 """


async def one(id: str):
    return await database.fetch_one(
        activity_audit.select().where(activity_audit.c.id == id)
    )


""" 根据活动ID获取审核记录 """


async def get_by_activity_id(activity_id: str):
    return await database.fetch_one(
        activity_audit.select().where(activity_audit.c.activity_id == activity_id)
    )


""" 更新审核状态 """


async def update_audit_status(id: str, status: str, opinion: str = None):
    try:
        values = {
            "audit_status": status,
            "audit_time": datetime.now(),
            "updated_at": datetime.now(),
        }
        if opinion:
            values["audit_remarks"] = opinion
        await database.execute(
            activity_audit.update().where(activity_audit.c.id == id).values(values)
        )
        return True
    except Exception:
        return False


""" 获取待审核活动列表 """


async def get_pending_audits():
    query = select(activity_audit).where(activity_audit.c.audit_status == "pending")
    return await database.fetch_all(query)


""" 获取审核统计 """


async def get_audit_statistics():
    try:
        status_query = select(
            activity_audit.c.audit_status,
            func.count(activity_audit.c.id).label("count"),
        ).group_by(activity_audit.c.audit_status)
        status_stats = await database.fetch_all(status_query)
        today = datetime.now().date()
        today_query = select(func.count(activity_audit.c.id)).where(
            func.date(activity_audit.c.audit_time) == today
        )
        today_count = await database.fetch_one(today_query)
        return {"status_stats": status_stats, "today_count": today_count.count_1 or 0}
    except Exception as err:
        logger.error(f"获取审核统计失败：{str(err)}", exc_info=True)
        return {"status_stats": [], "today_count": 0}
