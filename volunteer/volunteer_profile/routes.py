from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from utils.depends import auth, auth_name
from utils.result import Result

from .model import (
    VolunteerProfileBody,
    VolunteerProfileQuery,
    VolunteerProfileUpdateBody,
)
from .service import (
    add,
    delete,
    get_by_user_id,
    get_skills_statistics,
    get_volunteer_statistics,
    list_data,
    one,
    page_data,
    update,
    update_service_stats,
)

""" 志愿者档案管理 - 模块路由 """

volunteer_profile_route = APIRouter()


@volunteer_profile_route.get("/page")
async def _page(
    page: int,
    limit: int,
    user_name: str | None = None,
    volunteer_level: str | None = None,
    skills: str | None = None,
):
    if user_name != None:
        user_name = user_name + "#like"
    total, list = await page_data(
        page,
        limit,
        VolunteerProfileQuery(
            user_name=user_name, volunteer_level=volunteer_level, skills=skills
        ),
    )
    return Result.success(total=total, data=list)


@volunteer_profile_route.get("/list")
async def _list(user_name: str | None = None, volunteer_level: str | None = None):
    if user_name != None:
        user_name = user_name + "#like"
    data = await list_data(
        VolunteerProfileQuery(user_name=user_name, volunteer_level=volunteer_level)
    )
    # 修复：传递正确的total参数，确保前端能正确显示数据
    return Result.success(data=data, total=len(data))


@volunteer_profile_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data=await one(id))


@volunteer_profile_route.get("/user/{user_id}")
async def _get_by_user_id(user_id: str):
    return Result.success(data=await get_by_user_id(user_id))


@volunteer_profile_route.post("/add")
async def _add(_volunteerProfile: VolunteerProfileBody):
    try:
        print(f"接收到志愿者档案数据: {_volunteerProfile}")
        result = await add(_volunteerProfile)
        if result == True:
            return Result.success(data=result)
        return Result.fail(msg="添加志愿者档案失败，请检查数据是否完整或用户ID是否重复")
    except Exception as e:
        print(f"添加志愿者档案失败: {str(e)}")
        return Result.fail(msg=f"添加失败: {str(e)}")


# 移除错误的 exception_handler 装饰器
# 异常处理应该在应用级别定义


@volunteer_profile_route.put("/update/{id}")
async def _update(id: str, _volunteerProfile: VolunteerProfileUpdateBody):
    return Result.success(data=await update(id, _volunteerProfile))


@volunteer_profile_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@volunteer_profile_route.put("/stats/{user_id}")
async def _update_stats(user_id: str, service_hours: int, activity_count: int):
    result = await update_service_stats(user_id, service_hours, activity_count)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@volunteer_profile_route.get("/statistics")
async def _get_statistics():
    data = await get_volunteer_statistics()
    return Result.success(data=data)


@volunteer_profile_route.get("/skills/statistics")
async def _get_skills_statistics():
    data = await get_skills_statistics()
    return Result.success(data=data)
