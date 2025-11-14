from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from utils.depends import auth_name

from .model import (
    CheckInBody,
    CheckOutBody,
    ParticipationBody,
    ParticipationQuery,
    ParticipationUpdateBody,
)
from .service import (
    add,
    cancel_participation,
    check_in,
    check_out,
    delete,
    get_user_statistics,
    list_data,
    one,
    page_data,
    update,
)

""" 活动参与记录 - 模块路由 """

participation_route = APIRouter()


@participation_route.get("/page")
async def _page(
    page: int, limit: int, activity_name: str | None = None, status: str | None = None
):
    if activity_name is not None:
        activity_name = activity_name + "#like"
    total, list_data = await page_data(
        page, limit, ParticipationQuery(activity_name=activity_name, status=status)
    )
    # 符合Layui表格要求的响应格式
    return {"code": 0, "msg": "", "count": total, "data": list_data}


@participation_route.get("/list")
async def _list(activity_name: str | None = None, status: str | None = None):
    if activity_name is not None:
        activity_name = activity_name + "#like"
    data = await list_data(
        ParticipationQuery(activity_name=activity_name, status=status)
    )
    return {"code": 0, "msg": "", "count": len(data), "data": data}


@participation_route.get("/one/{id}")
async def _one(id: str):
    data = await one(id)
    if data:
        return {"code": 0, "msg": "", "data": data}
    else:
        return {"code": 1, "msg": "数据不存在", "data": None}


@participation_route.post("/add")
async def _add(
    _participation: ParticipationBody, current_user: Annotated[dict, Depends(auth_name)]
):
    result = await add(_participation, current_user)
    if result:
        return {"code": 0, "msg": "报名成功", "data": None}
    else:
        return {
            "code": 1,
            "msg": "报名失败，您可能已报名该活动或活动不存在",
            "data": None,
        }


@participation_route.put("/update/{id}")
async def _update(id: str, _participation: ParticipationUpdateBody):
    result = await update(id, _participation)
    if result:
        return {"code": 0, "msg": "更新成功", "data": None}
    else:
        return {"code": 1, "msg": "更新失败", "data": None}


@participation_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result:
        return {"code": 0, "msg": "删除成功", "data": None}
    else:
        return {"code": 1, "msg": "删除失败", "data": None}


@participation_route.post("/checkin/{id}")
async def _check_in(id: str, check_in_data: CheckInBody):
    result = await check_in(id, check_in_data.check_in_time)
    if result:
        return {"code": 0, "msg": "签到成功", "data": None}
    else:
        return {"code": 1, "msg": "签到失败，记录不存在或状态不正确", "data": None}


@participation_route.post("/checkout/{id}")
async def _check_out(id: str, check_out_data: CheckOutBody):
    result = await check_out(
        id, check_out_data.check_out_time, check_out_data.service_hours
    )
    if result:
        return {"code": 0, "msg": "签退成功", "data": None}
    else:
        return {"code": 1, "msg": "签退失败，记录不存在或状态不正确", "data": None}


@participation_route.post("/cancel/{id}")
async def _cancel(id: str):
    result = await cancel_participation(id)
    if result:
        return {"code": 0, "msg": "取消报名成功", "data": None}
    else:
        return {"code": 1, "msg": "取消报名失败，记录不存在或状态不正确", "data": None}


@participation_route.get("/statistics")
async def _statistics(current_user: Annotated[dict, Depends(auth_name)]):
    data = await get_user_statistics(current_user["user_id"])
    if data:
        return {"code": 0, "msg": "", "data": data}
    else:
        return {"code": 1, "msg": "获取统计数据失败", "data": None}
