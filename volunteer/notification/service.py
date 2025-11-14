import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    Text,
    delete,
    func,
    select,
    update,
)
from sqlalchemy.dialects.mysql import INTEGER

logger = logging.getLogger(__name__)

# ====================== 表结构定义 ======================
metadata = MetaData()

notification_table = Table(
    "notification",
    metadata,
    Column("id", String(36), primary_key=True, comment="通知ID"),
    Column("title", String(255), nullable=False, comment="消息标题"),
    Column("content", Text, nullable=False, comment="消息内容"),
    Column(
        "type",
        String(50),
        nullable=False,
        comment="消息类型: system, activity, reminder, announcement",
    ),
    Column(
        "priority", String(20), default="normal", comment="优先级: high, normal, low"
    ),
    Column("target_user_id", String(36), comment="目标用户ID，为空则发给所有用户"),
    Column("is_read", Boolean, default=False, comment="是否已读"),
    Column("is_sent", Boolean, default=False, comment="是否已发送"),
    Column("created_at", DateTime, default=datetime.now, comment="创建时间"),
    Column(
        "updated_at",
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    ),
    Column("read_at", DateTime, comment="阅读时间"),
    Column("sent_at", DateTime, comment="发送时间"),
)


# Pydantic 模型定义
class NotificationQuery(BaseModel):
    type: Optional[str] = None
    target_user_id: Optional[str] = None
    is_read: Optional[bool] = None
    priority: Optional[str] = None
    title: Optional[str] = None


class NotificationBody(BaseModel):
    title: str
    content: str
    type: str
    priority: Optional[str] = "normal"
    target_user_id: Optional[str] = None


# ===========================================================================
# 所有数据库操作函数都增加一个 database 参数
# ===========================================================================


async def page_data(
    database, page: int, limit: int, query_params: NotificationQuery
) -> tuple[int, List[Dict[str, Any]]]:
    """分页查询通知"""
    offset = (page - 1) * limit

    query = select(notification_table)
    if query_params.type:
        query = query.where(notification_table.c.type == query_params.type)
    if query_params.target_user_id:
        query = query.where(
            notification_table.c.target_user_id == query_params.target_user_id
        )
    if query_params.is_read is not None:
        query = query.where(notification_table.c.is_read == query_params.is_read)
    if query_params.priority:
        query = query.where(notification_table.c.priority == query_params.priority)
    if query_params.title:
        query = query.where(notification_table.c.title.ilike(f"%{query_params.title}%"))

    total_query = select(func.count()).select_from(notification_table)
    total = await database.fetch_val(total_query)

    query = (
        query.order_by(notification_table.c.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    results = await database.fetch_all(query)

    return total, [dict(result) for result in results]


async def list_data(database, query_params: NotificationQuery) -> List[Dict[str, Any]]:
    """查询通知列表"""
    query = select(notification_table)
    if query_params.type:
        query = query.where(notification_table.c.type == query_params.type)
    if query_params.target_user_id:
        query = query.where(
            notification_table.c.target_user_id == query_params.target_user_id
        )

    results = await database.fetch_all(query)
    return [dict(result) for result in results]


async def one(database, id: str) -> Optional[Dict[str, Any]]:
    """查询单个通知"""
    query = select(notification_table).where(notification_table.c.id == id)
    result = await database.fetch_one(query)
    return dict(result) if result else None


async def add(database, notification: NotificationBody) -> bool:
    """添加通知"""
    try:
        query = notification_table.insert().values(
            id=str(uuid.uuid4()),
            title=notification.title,
            content=notification.content,
            type=notification.type,
            priority=notification.priority,
            target_user_id=notification.target_user_id,
            is_read=False,
            is_sent=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"添加通知失败: {e}")
        return False


async def update(database, id: str, notification: NotificationBody) -> bool:
    """更新通知"""
    try:
        query = (
            notification_table.update()
            .where(notification_table.c.id == id)
            .values(
                title=notification.title,
                content=notification.content,
                type=notification.type,
                priority=notification.priority,
                target_user_id=notification.target_user_id,
                updated_at=datetime.now(),
            )
        )
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"更新通知失败: {e}")
        return False


async def delete(database, id: str) -> bool:
    """删除通知"""
    try:
        query = notification_table.delete().where(notification_table.c.id == id)
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"删除通知失败: {e}")
        return False


async def get_by_user_id(
    database, user_id: str, unread_only: bool = False
) -> List[Dict[str, Any]]:
    """根据用户ID查询通知"""
    query = select(notification_table).where(
        notification_table.c.target_user_id == user_id
    )
    if unread_only:
        query = query.where(notification_table.c.is_read == False)

    results = await database.fetch_all(query)
    return [dict(result) for result in results]


async def mark_as_read(database, id: str) -> bool:
    """标记通知为已读"""
    try:
        query = (
            notification_table.update()
            .where(notification_table.c.id == id)
            .values(is_read=True, read_at=datetime.now(), updated_at=datetime.now())
        )
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"标记通知为已读失败: {e}")
        return False


async def mark_multiple_as_read(database, ids: List[str]) -> bool:
    """批量标记通知为已读"""
    try:
        query = (
            notification_table.update()
            .where(notification_table.c.id.in_(ids))
            .values(is_read=True, read_at=datetime.now(), updated_at=datetime.now())
        )
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"批量标记通知为已读失败: {e}")
        return False


async def get_unread_count(database, user_id: str) -> int:
    """获取用户未读通知数量"""
    query = (
        select(func.count())
        .select_from(notification_table)
        .where(
            notification_table.c.target_user_id == user_id,
            notification_table.c.is_read == False,
        )
    )
    return await database.fetch_val(query)


async def get_notification_statistics(database) -> Dict[str, Any]:
    """获取通知统计数据"""
    try:
        type_query = select(
            notification_table.c.type,
            func.count(notification_table.c.id).label("count"),
        ).group_by(notification_table.c.type)
        type_stats = await database.fetch_all(type_query)

        priority_query = select(
            notification_table.c.priority,
            func.count(notification_table.c.id).label("count"),
        ).group_by(notification_table.c.priority)
        priority_stats = await database.fetch_all(priority_query)

        today = datetime.now().date()
        today_query = (
            select(func.count())
            .select_from(notification_table)
            .where(func.date(notification_table.c.created_at) == today)
        )
        today_count = await database.fetch_val(today_query)

        return {
            "type_stats": [dict(stat) for stat in type_stats],
            "priority_stats": [dict(stat) for stat in priority_stats],
            "today_count": today_count,
        }
    except Exception as err:
        logger.error(f"获取通知统计数据失败: {err}")
        return {"type_stats": [], "priority_stats": [], "today_count": 0}


async def send_system_notification(
    database, title: str, content: str, priority: str = "normal"
) -> bool:
    """发送系统通知"""
    try:
        query = notification_table.insert().values(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            type="system",
            priority=priority,
            is_read=False,
            is_sent=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            sent_at=datetime.now(),
        )
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"发送系统通知失败: {e}")
        return False


async def send_activity_notification(
    database, title: str, content: str, target_user_id: str, priority: str = "normal"
) -> bool:
    """发送活动通知"""
    try:
        query = notification_table.insert().values(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            type="activity",
            priority=priority,
            target_user_id=target_user_id,
            is_read=False,
            is_sent=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            sent_at=datetime.now(),
        )
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"发送活动通知失败: {e}")
        return False


async def query_notify_by_id(database, notify_id: str) -> Optional[Dict[str, Any]]:
    """根据ID查询通知详情（用于重发功能）"""
    query = select(notification_table).where(notification_table.c.id == notify_id)
    result = await database.fetch_one(query)
    return dict(result) if result else None


async def batch_delete(database, ids: List[str]) -> bool:
    """批量删除通知"""
    if not ids:
        return False
    try:
        query = notification_table.delete().where(notification_table.c.id.in_(ids))
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"批量删除通知失败: {e}")
        return False


async def batch_send(database, ids: List[str]) -> bool:
    """批量发送通知"""
    if not ids:
        return False
    try:
        query = (
            notification_table.update()
            .where(notification_table.c.id.in_(ids))
            .values(is_sent=True, sent_at=datetime.now(), updated_at=datetime.now())
        )
        await database.execute(query)
        return True
    except Exception as e:
        logger.error(f"批量发送通知失败: {e}")
        return False
