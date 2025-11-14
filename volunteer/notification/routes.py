import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Request

# 从 config 模块导入与主应用共享的 database 实例
from config import database

# 尝试导入通知查询函数（用于重发功能）
try:
    from .service import query_notify_by_id
except ImportError:
    query_notify_by_id = None

from utils.result import Result

from .model import NotificationBody, NotificationQuery, NotificationUpdateBody
from .service import add
from .service import batch_delete as service_batch_delete
from .service import batch_send as service_batch_send
from .service import (delete, get_by_user_id, get_notification_statistics,
                      get_unread_count, list_data, mark_as_read,
                      mark_multiple_as_read, one, page_data,
                      send_activity_notification, send_system_notification,
                      update)

""" 通知消息管理 - 模块路由 """
notification_route = APIRouter(tags=["Notification"])


# ---------------------- 基础CRUD接口 ----------------------
@notification_route.post("/page")
async def _page(request: Request):
    """分页查询（适配Layui表格的POST请求）"""
    try:
        body = await request.json()
    except Exception:
        body = dict(await request.form())

    page = int(body.get("page", 1))
    limit = int(body.get("limit", 10))

    query_params = NotificationQuery(
        type=body.get("type"),
        target_user_id=body.get("target_user_id"),
        is_read=body.get("is_read"),
        priority=body.get("priority"),
        title=body.get("title"),
    )

    # 将共享的 database 实例传递给 service 函数
    total, list_data = await page_data(database, page, limit, query_params)
    return Result.success(total=total, data=list_data)


@notification_route.get("/list")
async def _list(type: str | None = None, target_user_id: str | None = None):
    data = await list_data(
        database, NotificationQuery(type=type, target_user_id=target_user_id)
    )
    return Result.success(data=data)


@notification_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data=await one(database, id))


@notification_route.get("/user/{user_id}")
async def _get_by_user_id(user_id: str, unread_only: bool = False):
    data = await get_by_user_id(database, user_id, unread_only)
    return Result.success(data=data)


@notification_route.post("/add")
async def _add(_notification: NotificationBody):
    result = await add(database, _notification)
    return (
        Result.success(data=result, msg="添加成功")
        if result
        else Result.fail(msg="添加失败")
    )


@notification_route.put("/update/{id}")
async def _update(id: str, _notification: NotificationUpdateBody):
    update_data = _notification.dict(exclude_unset=True)
    if not update_data:
        return Result.fail(msg="没有需要更新的字段")

    current_notification = await one(database, id)
    if not current_notification:
        return Result.fail(msg="通知不存在")

    updated_notification_data = {**current_notification, **update_data}

    notification_to_update = NotificationBody(
        title=updated_notification_data["title"],
        content=updated_notification_data["content"],
        type=updated_notification_data["type"],
        priority=updated_notification_data.get("priority", "normal"),
        target_user_id=updated_notification_data.get("target_user_id"),
    )

    result = await update(database, id, notification_to_update)
    return (
        Result.success(data=result, msg="更新成功")
        if result
        else Result.fail(msg="更新失败")
    )


@notification_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(database, id)
    return (
        Result.success(data=result, msg="删除成功")
        if result
        else Result.fail(msg="删除失败")
    )


@notification_route.put("/read/{id}")
async def _mark_as_read(id: str):
    result = await mark_as_read(database, id)
    return (
        Result.success(data=result, msg="标记已读成功")
        if result
        else Result.fail(msg="标记已读失败")
    )


@notification_route.put("/read/multiple")
async def _mark_multiple_as_read(ids: List[str]):
    result = await mark_multiple_as_read(database, ids)
    return (
        Result.success(data=result, msg="批量标记已读成功")
        if result
        else Result.fail(msg="批量标记已读失败")
    )


@notification_route.get("/unread/count/{user_id}")
async def _get_unread_count(user_id: str):
    count = await get_unread_count(database, user_id)
    return Result.success(data={"unread_count": count})


@notification_route.get("/statistics")
async def _get_statistics():
    data = await get_notification_statistics(database)
    return Result.success(data=data)


# ---------------------- 原生发送接口 ----------------------
@notification_route.post("/send/system")
async def _send_system_notification(request: Request):
    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.json()
        else:
            body = dict(await request.form())
    except Exception as e:
        return Result.fail(msg=f"参数解析失败：{str(e)}")

    title = body.get("title", "").strip()
    content = body.get("content", "").strip()
    priority = body.get("priority", "normal")
    if not title or not content:
        return Result.fail(msg="标题和内容不能为空")

    result = await send_system_notification(database, title, content, priority)
    return (
        Result.success(data=result, msg="系统通知发送成功")
        if result
        else Result.fail(msg="系统通知发送失败")
    )


@notification_route.post("/send/activity")
async def _send_activity_notification(request: Request):
    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.json()
        else:
            body = dict(await request.form())
    except Exception as e:
        return Result.fail(msg=f"参数解析失败：{str(e)}")

    title = body.get("title", "").strip()
    content = body.get("content", "").strip()
    target_user_id = body.get("target_user_id", "").strip()
    priority = body.get("priority", "normal")
    if not title or not content or not target_user_id:
        return Result.fail(msg="标题、内容和目标用户ID不能为空")

    result = await send_activity_notification(
        database, title, content, target_user_id, priority
    )
    return (
        Result.success(data=result, msg="活动通知发送成功")
        if result
        else Result.fail(msg="活动通知发送失败")
    )


# ---------------------- 适配前端的接口 ----------------------
@notification_route.post("/send")
async def _send_notification_compat(request: Request):
    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.json()
        else:
            body = dict(await request.form())
    except Exception as e:
        return Result.fail(msg=f"请求参数格式错误：{str(e)}")

    title = body.get("title", "").strip()
    content = body.get("content", "").strip()
    if not title or not content:
        return Result.fail(msg="标题和内容不能为空")

    target_type = body.get("target_type", "all")
    role_ids = body.get("role_ids", [])
    user_ids = body.get("user_ids", "").strip()

    if target_type == "role" and role_ids:
        logging.info(f"准备向角色 {role_ids} 发送通知")
        result = await send_system_notification(
            database,
            title=title,
            content=content,
            priority=body.get("priority", "normal"),
        )
        return Result.success(data=result, msg=f"已向角色 {role_ids} 发送通知")

    elif target_type == "user" and user_ids:
        user_ids_list = user_ids.split(",")
        logging.info(f"准备向用户 {user_ids_list} 发送通知")
        if user_ids_list:
            result = await send_activity_notification(
                database,
                title=title,
                content=content,
                target_user_id=user_ids_list[0],
                priority=body.get("priority", "normal"),
            )
            return Result.success(data=result, msg=f"已向指定用户发送通知")

    else:  # target_type == "all"
        result = await send_system_notification(
            database,
            title=title,
            content=content,
            priority=body.get("priority", "normal"),
        )
        return (
            Result.success(data=result, msg="通知发送成功")
            if result
            else Result.fail(msg="通知发送失败")
        )


@notification_route.post("/delete")
async def _delete_notification_compat(request: Request):
    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.json()
        else:
            body = dict(await request.form())
    except Exception as e:
        return Result.fail(msg=f"请求参数格式错误：{str(e)}")

    notify_id = body.get("id")
    if not notify_id:
        return Result.fail(msg="请选择要删除的通知（未传入通知ID）")

    result = await delete(database, notify_id)
    return (
        Result.success(data=result, msg="通知删除成功")
        if result
        else Result.fail(msg="通知删除失败")
    )


@notification_route.post("/resend")
async def _resend_notification_compat(request: Request):
    if not query_notify_by_id:
        return Result.fail(msg="重发功能未启用（缺少通知查询依赖）")

    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.json()
        else:
            body = dict(await request.form())
    except Exception as e:
        return Result.fail(msg=f"请求参数格式错误：{str(e)}")

    notify_id = body.get("id")
    if not notify_id:
        return Result.fail(msg="请选择要重发的通知（未传入通知ID）")

    try:
        notify = await query_notify_by_id(database, notify_id)
        if not notify:
            return Result.fail(msg=f"通知不存在（ID：{notify_id}）")
    except Exception as e:
        return Result.fail(msg=f"查询通知失败：{str(e)}")

    if notify.get("type") == "activity" or notify.get("target_user_id"):
        result = await send_activity_notification(
            database,
            title=notify.get("title", ""),
            content=notify.get("content", ""),
            target_user_id=notify.get("target_user_id", ""),
            priority=notify.get("priority", "normal"),
        )
    else:
        result = await send_system_notification(
            database,
            title=notify.get("title", ""),
            content=notify.get("content", ""),
            priority=notify.get("priority", "normal"),
        )

    return (
        Result.success(data=result, msg="通知重发成功")
        if result
        else Result.fail(msg="通知重发失败")
    )


# ---------------------- 批量操作接口 ----------------------
@notification_route.post("/batch_send")
async def batch_send(request: Request):
    """批量发送通知"""
    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.json()
        else:
            body = dict(await request.form())
    except Exception as e:
        return Result.fail(msg=f"请求参数格式错误：{str(e)}")

    ids = body.get("ids")
    if not ids:
        return Result.fail(msg="请选择要发送的通知ID列表")

    if isinstance(ids, str):
        ids = ids.split(",")

    result = await service_batch_send(database, ids)
    return (
        Result.success(data=result, msg="批量发送成功")
        if result
        else Result.fail(msg="批量发送失败")
    )


@notification_route.post("/batch_delete")
async def batch_delete(request: Request):
    """批量删除通知"""
    try:
        if "application/json" in request.headers.get("content-type", ""):
            body = await request.json()
        else:
            body = dict(await request.form())
    except Exception as e:
        return Result.fail(msg=f"请求参数格式错误：{str(e)}")

    ids = body.get("ids")
    if not ids:
        return Result.fail(msg="请选择要删除的通知ID列表")

    if isinstance(ids, str):
        ids = ids.split(",")

    result = await service_batch_delete(database, ids)
    return (
        Result.success(data=result, msg="批量删除成功")
        if result
        else Result.fail(msg="批量删除失败")
    )
