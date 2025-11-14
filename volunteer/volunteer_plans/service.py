import logging
import uuid
from datetime import datetime

from sqlalchemy import func, select

from config import database, metadata

# 从共享表定义中导入
from config.tables import volunteer_plans
from utils.fix_query import FixQuery

from .model import VolunteerPlansBody, VolunteerPlansQuery, VolunteerPlansUpdateBody

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

""" 活动计划管理 - 功能CRUD模块 """

""" 分页查询 """


async def page_data(
    start: int = 1,
    limit: int = 10,
    query_volunteer_plans: VolunteerPlansQuery = None,
    current_user: dict = None,
):
    try:
        logger.info(f"查询活动计划，页码：{start}，每页：{limit}")
        base_query = select(volunteer_plans)
        total_query = select(func.count(volunteer_plans.c.id)).select_from(
            volunteer_plans
        )

        # --- 新增逻辑：根据当前用户角色过滤 ---
        if current_user and "role" in current_user:
            base_query = base_query.where(
                volunteer_plans.c.creator_role == current_user["role"]
            )
            total_query = total_query.where(
                volunteer_plans.c.creator_role == current_user["role"]
            )
        # -------------------------------------

        if query_volunteer_plans:
            total_query, base_query = FixQuery.query(
                query_volunteer_plans,
                val=query_volunteer_plans,
                instance=volunteer_plans,
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
        logger.error(f"查询活动计划失败：{str(e)}")
        return 0, []


""" 列表查询 """


async def list_data(
    query_volunteer_plans: VolunteerPlansQuery = None, current_user: dict = None
):
    try:
        logger.info("查询活动计划列表")
        base_query = select(volunteer_plans)

        # --- 新增逻辑：根据当前用户角色过滤 ---
        if current_user and "role" in current_user:
            base_query = base_query.where(
                volunteer_plans.c.creator_role == current_user["role"]
            )
        # -------------------------------------

        if query_volunteer_plans:
            _, base_query = FixQuery.query(
                query_volunteer_plans,
                val=query_volunteer_plans,
                instance=volunteer_plans,
                total_query=select(func.count(volunteer_plans.c.id)),
                query=base_query,
            )
        list_data = await database.fetch_all(base_query)
        logger.info(f"查询成功，返回数据：{len(list_data)}")
        return list_data
    except Exception as e:
        logger.error(f"查询活动计划列表失败：{str(e)}")
        return []


""" 根据主键进行删除 """


async def delete(id: str):
    try:
        await database.execute(
            volunteer_plans.delete().where(volunteer_plans.c.id == id)
        )
        return True
    except Exception:
        return False


""" 添加 """


async def add(_volunteer_plans: VolunteerPlansBody, user_info: any):
    activity_data = _volunteer_plans.dict()

    # 准备插入活动计划表的数据
    values = {
        "id": str(uuid.uuid4()),
        "activity_name": activity_data["activity_name"],
        "activity_date": activity_data["activity_date"],
        "activity_type": activity_data["activity_type"],
        "location": activity_data["location"],
        "service_hours": activity_data["service_hours"],
        "max_participants": activity_data["max_participants"],
        "requirements": activity_data.get("requirements", ""),
        "benefits": activity_data.get("benefits", ""),
        "contact_person": activity_data.get("contact_person", ""),
        "contact_phone": activity_data.get("contact_phone", ""),
        "remark": activity_data.get("remark", ""),
        "user_id": user_info["user_id"],
        "user_name": user_info["nick_name"],
        "creator_role": user_info.get("role", "user"),  # <--- 新增：记录创建者角色
        "status": "draft",  # 先设为草稿
        "current_participants": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }

    try:
        # 1. 先创建活动计划记录（状态为 draft）
        await database.execute(volunteer_plans.insert().values(values))
        logger.info(
            f"活动计划 '{values['activity_name']}' 创建成功，ID: {values['id']}，状态: draft"
        )

        # 2. 立即将活动状态更新为 'pending'（待审核）
        status_updated = await update_status(values["id"], "pending")
        if status_updated:
            logger.info(
                f"活动 '{values['activity_name']}' 状态已从 draft 更新为 pending。"
            )
        else:
            logger.error(f"活动 '{values['activity_name']}' 状态更新失败！")
            return False

        # 3. 同步创建审核记录
        logger.info(f"为活动 '{values['activity_name']}' 创建审核记录...")

        from volunteer.activity_audit.model import ActivityAuditBody
        from volunteer.activity_audit.service import add as add_audit_record

        # 构造完整的审核记录数据
        audit_record_data = ActivityAuditBody(
            activity_id=values["id"],
            activity_name=values["activity_name"],
            activity_type=values["activity_type"],
            organizer_name=values["user_name"],
            organizer_phone=values["contact_phone"],
            activity_location=values["location"],
            start_time=values["activity_date"],
            end_time=values["activity_date"],
            expected_participants=values["max_participants"],
            activity_description=values["remark"],
            audit_status="pending",
        )

        # 调用审核模块的添加函数
        audit_result = await add_audit_record(audit_record_data, user_info)

        if audit_result:
            logger.info(f"活动 '{values['activity_name']}' 的审核记录创建成功。")
        else:
            logger.error(f"活动 '{values['activity_name']}' 的审核记录创建失败！")
            # 回滚活动状态
            await update_status(values["id"], "draft")
            return False

        return True

    except Exception as err:
        logger.error(f"创建活动计划失败：{str(err)}", exc_info=True)
        return False


""" 修改 """


async def update(id: str, _volunteer_plans: VolunteerPlansUpdateBody):
    values = _volunteer_plans.dict(exclude_unset=True)
    values["updated_at"] = datetime.now()
    try:
        await database.execute(
            volunteer_plans.update().where(volunteer_plans.c.id == id).values(values)
        )
        return True
    except Exception:
        return False


""" 根据主键获取单条数据 """


async def one(id: str):
    return await database.fetch_one(
        volunteer_plans.select().where(volunteer_plans.c.id == id)
    )


""" 更新活动状态 """


async def update_status(id: str, status: str):
    try:
        await database.execute(
            volunteer_plans.update()
            .where(volunteer_plans.c.id == id)
            .values({"status": status, "updated_at": datetime.now()})
        )
        return True
    except Exception:
        return False


""" 更新报名人数 """


async def update_participant_count(id: str, count: int):
    try:
        await database.execute(
            volunteer_plans.update()
            .where(volunteer_plans.c.id == id)
            .values({"current_participants": count, "updated_at": datetime.now()})
        )
        return True
    except Exception:
        return False
