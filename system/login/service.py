from system.menu.service import get_menu
from system.user.model import UserBody
from system.user.service import add, one, username
from system.user_role.service import lists as lists_role
from utils.depends import generate_jwt_token
from utils.passwd import (get_password_hash, rsa_decrypt_password,
                          verify_password)
from utils.result import Result

from .model import LoginBody, RegisterBody

""" 登录功能模块 """


async def login(_login: LoginBody):
    try:
        user = await username(_login.username)
        if user.status == 0:
            return Result.success(data="用户已被禁用")
        if verify_password(rsa_decrypt_password(_login.password), user.password):
            return Result.success(
                data=generate_jwt_token(
                    {"user_id": user.id, "nick_name": user.nick_name}
                )
            )
    except Exception as err:
        print(err)
        pass
    return Result.fail(data="用户名或密码错误")


async def login_plaintext(username_str: str, password_str: str):
    """明文密码登录（仅用于测试）"""
    try:
        user = await username(username_str)
        if not user:
            return Result.fail(data="用户不存在")
        if user.status == 0:
            return Result.fail(data="用户已被禁用")

        # 直接验证明文密码
        if verify_password(password_str, user.password):
            return Result.success(
                data=generate_jwt_token(
                    {"user_id": user.id, "nick_name": user.nick_name}
                )
            )
        else:
            return Result.fail(data="密码错误")
    except Exception as err:
        print(f"Login error: {err}")
        return Result.fail(data="登录失败")


async def register(_register: RegisterBody):
    try:
        user = await username(_register.username)
        if user is None:
            flag = await add(
                UserBody(
                    nick_name=_register.nickname,
                    gender="1",
                    username=_register.username,
                    password=_register.password,
                    status="1",
                    role_ids="b2168c4f-b972-4d05-ad1b-ff8558c04388",
                )
            )
            if flag == True:
                return Result.success(data="注册成功")
    except Exception as err:
        print(err)
        pass
    return Result.fail(data="用户名已存在")


async def myinfo(user_id: str):
    try:
        _user = await one(user_id)
        _menus = await get_menu(user_id)
        _lists_role = await lists_role(user_id)
        result = Result.encoder(_user)
        result_menu = Result.encoder(_menus)
        result_role = Result.encoder(_lists_role)
        del result["password"]
        result["menus"] = Result.generate_tree_menu(result_menu, True)
        result["role_ids"] = [item["role_id"] for item in result_role]
        return Result.success(data=result)
    except Exception:
        pass
    return Result.fail(data="信息获取失败")
