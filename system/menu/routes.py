
from fastapi import APIRouter, Depends
from .service import pages, add, delete, update, one, lists
from .model import Menu, MenuQuery, MenuBody
from utils.result import Result
from typing import Annotated
from utils.depends import auth
from fastapi.encoders import jsonable_encoder

""" 菜单表 - 模块路由 """

menu_route = APIRouter()

@menu_route.get("/tree")
async def _tree(name: str|None=None):
    _data = await lists(MenuQuery(menu_name=name))
    return Result.success(data=Result.generate_tree_menu(Result.encoder(_data)))

@menu_route.get("/page")
async def _page(page: int, limit: int, name: str|None=None):
    total, list = await pages(page, limit, MenuQuery(name=name))
    return Result.success(total=total, data=list)

@menu_route.get("/one/{id}")
async def _one(id: str):
    return Result.success(data = await one(id))

@menu_route.post("/add")
async def _add(_menu: MenuBody, user_id: Annotated[str, Depends(auth)]):
    result = await add(_menu)
    if result == True:
        return Result.success(data=result )
    return Result.fail(data=result )

@menu_route.put("/update/{id}")
async def _update(id: str, _menu: MenuBody, user_id: Annotated[str, Depends(auth)]):
    return Result.success(data = await update(id, _menu))

@menu_route.delete("/delete/{id}")
async def _delete(id: str):
    result = await delete(id)
    if result == True:
        return Result.success(data=result )
    return Result.fail(data=result )

    