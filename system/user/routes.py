
from fastapi import APIRouter, Depends, Form
from .service import pages, add, delete, update, one, auth_role, upd_password
from .model import User, UserQuery, UserBody, UpPwdBody
from utils.result import Result
from typing import Annotated
from utils.depends import auth

""" 人员表 - 模块路由 """

user_route = APIRouter()

@user_route.get("/page")
async def _page(page: int, limit: int, nick_name: str|None=None):
    total, list = await pages(page, limit, UserQuery(nick_name=nick_name))
    return Result.success(total=total, data=list)

@user_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data = await one(id))

@user_route.post("/add")
async def _add(_user: UserBody, user_id: Annotated[str, Depends(auth)]):
    result = await add(_user)
    if result == True:
        return Result.success(data=result )
    return Result.fail(data=result )

@user_route.put("/update/{id}")
async def _update(id: str, _user: UserBody, user_id: Annotated[str, Depends(auth)]):
    result = await update(id, _user)
    if result == True:
        return Result.success(data=result )
    return Result.fail(data=result )

@user_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result == True:
        return Result.success(data=result )
    return Result.fail(data=result )

@user_route.post("/auth_role")
async def _authorize(user_id: Annotated[str, Form()], role_ids: Annotated[list[str], Form()]):
    return Result.success(data = await auth_role(user_id, role_ids))

@user_route.put("/password/{id}")
async def _update(id: str, _user: UpPwdBody):
    result = await upd_password(id, _user)
    return result
