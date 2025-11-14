from fastapi import Depends, FastAPI

from config import global_config
from utils.depends import auth

from .login.routes import login_route
from .menu.routes import menu_route
from .role.routes import role_route
from .user.routes import user_route

""" 注册路由 """


def register_sys_router(app: FastAPI):
    """菜单表"""
    app.include_router(
        menu_route,
        prefix=f"{global_config['prefix']}menu",
        tags=["Menu"],
        dependencies=[Depends(auth)],
    )
    """ 角色表 """
    app.include_router(
        role_route,
        prefix=f"{global_config['prefix']}role",
        tags=["Role"],
        dependencies=[Depends(auth)],
    )
    """ 人员表 """
    app.include_router(
        user_route,
        prefix=f"{global_config['prefix']}user",
        tags=["User"],
        dependencies=[Depends(auth)],
    )

    """ 登录 """
    app.include_router(login_route, tags=["Login"])
