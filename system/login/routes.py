import json
import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from config import global_config, templates
from system.menu.service import one as menu_one
from utils.depends import auth
from utils.result import Result

from .model import LoginBody, RegisterBody
from .service import login, login_plaintext, myinfo, register

""" 登录模块路由 """

login_route = APIRouter()


@login_route.post("/login")
async def plogin(loginBody: LoginBody, response: Response):
    result = await login(loginBody)
    if result["success"] == True:
        response.set_cookie(
            key="token", value=result["data"], expires=24 * 60 * 60, httponly=False
        )
    return result


@login_route.post("/login-test")
async def login_test(username: str, password: str, response: Response):
    """明文密码登录测试接口"""
    result = await login_plaintext(username, password)
    if result["success"] == True:
        response.set_cookie(
            key="token", value=result["data"], expires=24 * 60 * 60, httponly=False
        )
    return result


@login_route.post("/register")
async def _register(_register: RegisterBody):
    return await register(_register)


@login_route.get("/myinfo")
async def _myinfo(user_id: Annotated[str, Depends(auth)]):
    return await myinfo(user_id)


@login_route.get("/logout", response_class=HTMLResponse)
async def _logout(request: Request, response: Response):
    response.set_cookie(key="token", value="", httponly=False)
    return RedirectResponse("/login")


@login_route.get("/login", response_class=HTMLResponse)
async def to_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"sysname": global_config["sysname"]},
    )


@login_route.get("/flogout", response_class=HTMLResponse)
async def _logout(request: Request, response: Response):
    response.set_cookie(key="token", value="", httponly=False)
    return RedirectResponse("/flogin")


@login_route.get("/flogin", response_class=HTMLResponse)
async def to_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="front/login.html",
        context={"sysname": global_config["sysname"]},
    )


@login_route.get("/register", response_class=HTMLResponse)
async def _register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"sysname": global_config["sysname"]},
    )


@login_route.get("/", response_class=HTMLResponse)
async def index(request: Request, user_id: Annotated[str, Depends(auth)]):
    result = await myinfo(user_id)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": json.dumps(result["data"], ensure_ascii=False),
            "nick_name": result["data"]["nick_name"],
            "menus": result["data"]["menus"],
            "menu": result["data"]["menus"][0],
            "sysname": global_config["sysname"],
        },
    )


@login_route.get("/html/{menu_id}", response_class=HTMLResponse)
async def html_render(
    request: Request, menu_id: str, user_id: Annotated[str, Depends(auth)]
):
    result = await menu_one(menu_id)
    d_result = Result.encoder(result)
    return templates.TemplateResponse(
        request=request, name=d_result["hurl"], context={}
    )


@login_route.post("/upload")
async def upload(file: UploadFile):
    upload_dir = global_config["upload"]
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建项目根目录的路径 (假设项目根目录是 sports 目录的父目录)
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    # 构建完整的上传路径
    upload_path = os.path.join(project_root, upload_dir)

    # 确保上传目录存在
    os.makedirs(upload_path, exist_ok=True)

    file_location = os.path.join(upload_path, f"{uuid.uuid4()}-{file.filename}")
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return Result.success(
        data={
            "url": file_location.replace(project_root, "").replace(
                "\\", "/"
            ),  # 返回相对路径，并统一斜杠方向
            "mimeType": file.content_type,
        }
    )


@login_route.post("/upload-url")
async def uploadUrl(file: UploadFile):
    upload_dir = global_config["upload"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    upload_path = os.path.join(project_root, upload_dir)
    os.makedirs(upload_path, exist_ok=True)

    file_location = os.path.join(upload_path, f"{uuid.uuid4()}-{file.filename}")
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return Result.success(
        data=file_location.replace(project_root, "").replace("\\", "/")
    )


@login_route.post("/upload-200")
async def uploadUrl(file: UploadFile):
    upload_dir = global_config["upload"]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    upload_path = os.path.join(project_root, upload_dir)
    os.makedirs(upload_path, exist_ok=True)

    file_location = os.path.join(upload_path, f"{uuid.uuid4()}-{file.filename}")
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return Result.success(
        data={"url": file_location.replace(project_root, "").replace("\\", "/")},
        code=200,
    )
