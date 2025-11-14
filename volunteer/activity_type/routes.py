from typing import Annotated

from fastapi import APIRouter, Depends

from utils.depends import auth, auth_name
from utils.result import Result

from .model import ActivityTypeBody, ActivityTypeQuery, ActivityTypeUpdateBody
from .service import add, delete, list_data, one, page_data, update

""" 活动类型管理 - 模块路由 """

activity_type_route = APIRouter()


@activity_type_route.get("/page")
async def _page(
    page: int,
    limit: int,
    type_name: str | None = None,
    difficulty_level: str | None = None,
):
    if type_name != None:
        type_name = type_name + "#like"
    total, list = await page_data(
        page,
        limit,
        ActivityTypeQuery(type_name=type_name, difficulty_level=difficulty_level),
    )
    return Result.success(total=total, data=list)


@activity_type_route.get("/list")
async def _list(type_name: str | None = None, difficulty_level: str | None = None):
    if type_name != None:
        type_name = type_name + "#like"
    data = await list_data(
        ActivityTypeQuery(type_name=type_name, difficulty_level=difficulty_level)
    )
    # 修复：传递正确的total参数，确保前端能正确显示数据
    return Result.success(data=data, total=len(data))


@activity_type_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data=await one(id))


@activity_type_route.post("/add")
async def _add(_activityType: ActivityTypeBody):
    result = await add(_activityType)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@activity_type_route.put("/update/{id}")
async def _update(id: str, _activityType: ActivityTypeUpdateBody):
    return Result.success(data=await update(id, _activityType))


@activity_type_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)
