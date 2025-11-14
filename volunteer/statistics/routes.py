from typing import Annotated

from fastapi import APIRouter, Depends, Query

from utils.depends import auth
from utils.result import Result

from .model import StatisticsQuery
from .service import (get_activity_type_statistics, get_monthly_statistics,
                      get_user_statistics, get_volunteer_statistics)

""" 统计报表 - 模块路由 """

statistics_route = APIRouter()


@statistics_route.get("/volunteer")
async def _get_volunteer_statistics(
    start_date: str | None = None, end_date: str | None = None
):
    """获取志愿者统计信息"""
    query = None
    if start_date or end_date:
        query = StatisticsQuery(start_date=start_date, end_date=end_date)

    data = await get_volunteer_statistics(query)
    return Result.success(data=data)


@statistics_route.get("/activity_type")
async def _get_activity_type_statistics(
    start_date: str | None = None, end_date: str | None = None
):
    """获取活动类型统计信息"""
    query = None
    if start_date or end_date:
        query = StatisticsQuery(start_date=start_date, end_date=end_date)

    data = await get_activity_type_statistics(query)
    return Result.success(data=data)


@statistics_route.get("/user")
async def _get_user_statistics(
    start_date: str | None = None,
    end_date: str | None = None,
    user_id: str | None = None,
):
    """获取用户统计信息"""
    query = None
    if start_date or end_date or user_id:
        query = StatisticsQuery(
            start_date=start_date, end_date=end_date, user_id=user_id
        )

    data = await get_user_statistics(query)
    return Result.success(data=data)


@statistics_route.get("/monthly/{year}/{month}")
async def _get_monthly_statistics(year: int, month: int):
    """获取月度统计信息"""
    data = await get_monthly_statistics(year, month)
    return Result.success(data=data)


@statistics_route.get("/dashboard")
async def _get_dashboard_statistics():
    """获取仪表板统计信息"""
    # 获取基础统计
    volunteer_stats = await get_volunteer_statistics()

    # 获取活动类型统计
    activity_type_stats = await get_activity_type_statistics()

    # 获取月度统计（当前月）
    from datetime import datetime

    now = datetime.now()
    monthly_stats = await get_monthly_statistics(now.year, now.month)

    dashboard_data = {
        "volunteer_stats": volunteer_stats,
        "activity_type_stats": activity_type_stats,
        "monthly_stats": monthly_stats,
    }

    return Result.success(data=dashboard_data)
