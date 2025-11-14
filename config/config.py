import os
from pathlib import Path

import yaml
from fastapi.templating import Jinja2Templates

with open("config.yml", "r", encoding="utf-8") as file:
    global_config = yaml.safe_load(file)

templates = Jinja2Templates(directory=global_config["templates"])

from databases import Database

# 优先从环境变量读取数据库配置
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_NAME = os.getenv("DB_NAME", "volunteer")

# 构建数据库连接URL
if os.getenv("DB_URL"):
    # 如果设置了DB_URL环境变量，直接使用
    DB_URL = os.getenv("DB_URL")
else:
    # 否则使用环境变量构建
    DB_URL = (
        f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
    )

database = Database(DB_URL)
from sqlalchemy import MetaData

metadata = MetaData()
