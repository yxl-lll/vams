import time
import typing

import jwt
from fastapi import HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

from config import global_config


def auth(request: Request):
    # 优先从cookies获取token
    token = request.cookies.get("token")
    print(f"Cookie token: {token}")

    # 如果cookies中没有，尝试从Authorization header获取
    if token is None:
        auth_header = request.headers.get("Authorization")
        print(f"Auth header: {auth_header}")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]  # 去掉 'Bearer ' 前缀
            print(f"Extracted token from header: {token}")

    # 如果header中也没有，尝试从查询参数获取
    if token is None:
        token = request.query_params.get("_token")
        print(f"Token from query: {token}")

    if token is None:
        print("No token found, raising 401")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="token is notfund",
        )
    verify, data = verify_jwt_token(token)
    print(f"Token verification: {verify}, data: {data}")
    if verify is False:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=data,
        )
    return data["user_id"]


def auth_name(request: Request):
    # 优先从cookies获取token
    token = request.cookies.get("token")

    # 如果cookies中没有，尝试从Authorization header获取
    if token is None:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]  # 去掉 'Bearer ' 前缀

    # 如果header中也没有，尝试从查询参数获取
    if token is None:
        token = request.query_params.get("_token")

    if token is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="token is notfund",
        )
    verify, data = verify_jwt_token(token)
    if verify is False:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=data,
        )
    return data


# 密钥，用于签名和验证JWT


JWT_TOKEN_EXPIRE_TIME = 3600 * 2  # token有效时间 2小时
JWT_SECRET = (
    "5281d79b8c62299614597794fee315d493b252473ae290a8cd5db9b09052779d"  # 加解密密钥
)
JWT_ALGORITHM = "HS256"  # 加解密算法


def generate_jwt_token(user: typing.Any) -> str:
    """根据用户id生成token"""
    user["exp"] = int(time.time()) + JWT_TOKEN_EXPIRE_TIME
    token = jwt.encode(user, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token: str) -> bool:
    """验证用户token"""
    # return True, {"user_id":"001", "name":"temp"}
    try:
        _payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return False, "token解析失败"
    else:
        exp = int(_payload.pop("exp"))
        if time.time() > exp:
            return False, "已失效"
        return True, _payload


# print(generate_jwt_token('111'))
