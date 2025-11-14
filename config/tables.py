from sqlalchemy import Table, Column, Integer, String, DATETIME, Text, DECIMAL
from config import metadata

"""
集中管理所有数据库表结构定义，供各个service模块导入使用。
"""

# 活动计划表
volunteer_plans = Table(
    "volunteer_plans",
    metadata,
    Column("id", String, primary_key=True),
    Column("activity_name", String),
    Column("activity_date", DATETIME),
    Column("activity_type", String),
    Column("location", String),
    Column("service_hours", DECIMAL(5, 2)),
    Column("max_participants", Integer),
    Column("current_participants", Integer),
    Column("status", String),  # draft, pending, approved, ongoing, completed, cancelled
    Column("requirements", Text),
    Column("benefits", Text),
    Column("contact_person", String),
    Column("contact_phone", String),
    Column("remark", Text),
    Column("user_id", String),
    Column("user_name", String),
    Column("created_at", DATETIME),
    Column("updated_at", DATETIME),
    Column("creator_role", String),  # 新增：创建者角色
)

# 活动参与记录表
participation = Table(
    "participation",
    metadata,
    Column("id", String, primary_key=True),
    Column("activity_id", String),
    Column("activity_name", String),
    Column("activity_image", String),
    Column("activity_date", DATETIME),
    Column("activity_type", String),
    Column("service_hours", DECIMAL(5, 2)),
    Column("participant_count", Integer),
    Column("check_in_time", DATETIME),
    Column("check_out_time", DATETIME),
    Column("status", String),  # registered, checked_in, completed, cancelled
    Column("remark", String),
    Column("user_id", String),
    Column("user_name", String),
    Column("created_at", DATETIME),
    Column("updated_at", DATETIME),
)
