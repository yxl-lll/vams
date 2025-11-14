from typing import Annotated

from fastapi import APIRouter, Depends, Form

from utils.depends import auth
from utils.result import Result

from .model import Role, RoleBody, RoleQuery
from .service import (add, authorize, delete, get_auth_menu, get_auth_role,
                      lists, one, pages, update)

""" 角色表 - 模块路由 """

role_route = APIRouter()


@role_route.get("/list")
async def _list(name: str | None = None):
    _data = await lists(RoleQuery(menu_name=name))
    return Result.success(data=_data)


@role_route.get("/page")
async def _page(page: int, limit: int, name: str | None = None):
    total, list = await pages(page, limit, RoleQuery(role_name=name))
    return Result.success(total=total, data=list)


@role_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data=await one(id))


@role_route.post("/add")
async def _add(_role: RoleBody, user_id: Annotated[str, Depends(auth)]):
    result = await add(_role)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@role_route.put("/update/{id}")
async def _update(id: str, _role: RoleBody, user_id: Annotated[str, Depends(auth)]):
    return Result.success(data=await update(id, _role))


@role_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result == True:
        return Result.success(data=result)
    return Result.fail(data=result)


@role_route.post("/auth_menu")
async def _authorize(
    role_id: Annotated[str, Form()], menu_ids: Annotated[list[str], Form()]
):
    return Result.success(data=await authorize(role_id, menu_ids))


@role_route.get("/auth_menu")
async def _get_auth_menu(role_id: str | None = None):
    menus, menu_ids = await get_auth_menu(role_id)
    return Result.success(
        data={
            "menu_ids": menu_ids,
            "menus": Result.generate_tree_menu(Result.encoder(menus)),
        }
    )


@role_route.get("/auth_role")
async def _get_auth_role(user_id: str | None = None):
    roles, role_ids = await get_auth_role(user_id)
    return Result.success(data={"role_ids": role_ids, "roles": roles})
