from fastapi import APIRouter, Depends
from .service import page_data, add, delete, update, one, list_data, update_status
from .model import VolunteerPlansQuery, VolunteerPlansBody, VolunteerPlansUpdateBody, VolunteerPlansStatusUpdate
from utils.result import Result
from typing import Annotated, Optional
from utils.depends import auth, auth_name  # <--- 确保导入了 auth

""" 活动计划管理 - 模块路由 """

volunteer_plans_route = APIRouter()

# <--- 修改：增加 current_user 依赖，并传递给 page_data --->
@volunteer_plans_route.get("/page")
async def _page(page: int, limit: int, activity_name: Optional[str] = None, activity_type: Optional[str] = None, user_id: Optional[str] = None, status: Optional[str] = None, current_user: Annotated[dict, Depends(auth)] = None):
    query_params = VolunteerPlansQuery()
    if activity_name:
        query_params.activity_name = activity_name + "#like"
    if activity_type:
        query_params.activity_type = activity_type
    if user_id:
        query_params.user_id = user_id
    if status:
        query_params.status = status
        
    total, list_data = await page_data(page, limit, query_params, current_user) # <--- 传递 current_user
    return Result.success(total=total, data=list_data)

# <--- 修改：增加 current_user 依赖，并传递给 list_data --->
@volunteer_plans_route.get("/list")
async def _list(current_user: Annotated[dict, Depends(auth)], activity_name: Optional[str] = None, activity_type: Optional[str] = None, user_id: Optional[str] = None):
    query_params = VolunteerPlansQuery(user_id=user_id)
    if activity_name:
        query_params.activity_name = activity_name + "#like"
    if activity_type:
        query_params.activity_type = activity_type
        
    data = await list_data(query_params, current_user) # <--- 传递 current_user
    return Result.success(data=data, total=len(data))

@volunteer_plans_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data=await one(id))

@volunteer_plans_route.post("/add")
async def _add(_volunteerPlans: VolunteerPlansBody, user_info: Annotated[any, Depends(auth_name)]):
    result = await add(_volunteerPlans, user_info)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)

@volunteer_plans_route.put("/update/{id}")
async def _update(id: str, _volunteerPlans: VolunteerPlansUpdateBody, user_info: Annotated[any, Depends(auth_name)]):
    return Result.success(data=await update(id, _volunteerPlans))

@volunteer_plans_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)

@volunteer_plans_route.put("/status/{id}")
async def _update_status(id: str, status_data: VolunteerPlansStatusUpdate):
    result = await update_status(id, status_data.status)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)
