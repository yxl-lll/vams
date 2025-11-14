from fastapi import Depends, FastAPI

from config import global_config
from utils.depends import auth

from .activity_audit.routes import activity_audit_route
from .activity_type.routes import activity_type_route
from .notification.routes import notification_route
from .participation.routes import participation_route
from .statistics.routes import statistics_route
from .volunteer_plans.routes import volunteer_plans_route
from .volunteer_profile.routes import volunteer_profile_route

""" 注册路由 """


def register_volunteer_router(app: FastAPI):
    """活动计划管理"""
    app.include_router(
        volunteer_plans_route,
        prefix=f"{global_config['prefix']}volunteer_plans",
        tags=["VolunteerPlans"],
        dependencies=[Depends(auth)],
    )  # 统一缩进：4个空格
    """ 活动参与记录 """
    app.include_router(
        participation_route,
        prefix=f"{global_config['prefix']}participation",
        tags=["Participation"],
        dependencies=[Depends(auth)],
    )  # 统一缩进：4个空格
    """ 活动类型分类 """
    app.include_router(
        activity_type_route,
        prefix=f"{global_config['prefix']}activity_type",
        tags=["ActivityType"],
        dependencies=[Depends(auth)],
    )  # 统一缩进：4个空格
    """ 活动审核管理 """
    app.include_router(
        activity_audit_route,
        prefix=f"{global_config['prefix']}activity_audit",
        tags=["ActivityAudit"],
        dependencies=[Depends(auth)],
    )  # 统一缩进：4个空格
    """ 志愿者档案管理 """
    app.include_router(
        volunteer_profile_route,
        prefix=f"{global_config['prefix']}volunteer_profile",
        tags=["VolunteerProfile"],
        dependencies=[Depends(auth)],
    )  # 统一缩进：4个空格
    """ 通知消息管理 """
    app.include_router(
        notification_route,
        prefix=f"{global_config['prefix']}notification",
        tags=["Notification"],
        dependencies=[Depends(auth)],
    )  # 关键修正：和上面保持一致的4个空格缩进
    """ 统计报表 """
    app.include_router(
        statistics_route,
        prefix=f"{global_config['prefix']}statistics",
        tags=["Statistics"],
        dependencies=[Depends(auth)],
    )  # 统一缩进：4个空格
