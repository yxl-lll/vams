from fastapi import APIRouter, Depends
from .service import page_data, add, delete, update, one, list_data, update_audit_status, get_pending_audits, get_audit_statistics
from .model import ActivityAuditQuery, ActivityAuditBody, ActivityAuditUpdateBody, ActivityAuditStatusUpdate
from utils.result import Result
from typing import Annotated
from utils.depends import auth, auth_name

""" 活动审核管理 - 模块路由 """

activity_audit_route = APIRouter()


@activity_audit_route.get("/page")
async def _page(page: int, limit: int, activity_name: str | None = None, audit_status: str | None = None, auditor_id: str | None = None):
    if activity_name != None:
        activity_name = activity_name + "#like"
    total, list = await page_data(page, limit, ActivityAuditQuery(activity_name=activity_name, audit_status=audit_status, auditor_id=auditor_id))
    return Result.success(total=total, data=list)


@activity_audit_route.get("/list")
async def _list(activity_name: str | None = None, audit_status: str | None = None):
    if activity_name != None:
        activity_name = activity_name + "#like"
    data = await list_data(ActivityAuditQuery(activity_name=activity_name, audit_status=audit_status))
    # 修复：传递正确的total参数，确保前端能正确显示数据
    return Result.success(data=data, total=len(data))


@activity_audit_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data=await one(id))


@activity_audit_route.post("/add")
async def _add(_activityAudit: ActivityAuditBody, auditor_info: Annotated[any, Depends(auth_name)]):
    result = await add(_activityAudit, auditor_info)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@activity_audit_route.put("/update/{id}")
async def _update(id: str, _activityAudit: ActivityAuditUpdateBody):
    return Result.success(data=await update(id, _activityAudit))


@activity_audit_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@activity_audit_route.put("/status/{id}")
async def _update_status(id: str, status_data: ActivityAuditStatusUpdate):
    result = await update_audit_status(id, status_data.status, status_data.opinion)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@activity_audit_route.get("/pending")
async def _get_pending():
    data = await get_pending_audits()
    return Result.success(data=data)


@activity_audit_route.get("/statistics")
async def _get_statistics():
    data = await get_audit_statistics()
    return Result.success(data=data)
