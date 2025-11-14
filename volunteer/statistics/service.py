import logging
from datetime import date, datetime

from sqlalchemy import and_, func, select

from config import database
from volunteer.activity_type.service import activity_type
from volunteer.participation.service import participation
from volunteer.volunteer_plans.service import volunteer_plans
from volunteer.volunteer_profile.service import volunteer_profile

from .model import (
    ActivityStatistics,
    StatisticsQuery,
    UserStatistics,
    VolunteerStatistics,
)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

""" 统计报表 - 功能模块 """


async def get_volunteer_statistics(query: StatisticsQuery = None):
    """获取志愿者统计信息"""
    try:
        logger.info("获取志愿者统计信息")

        # 统计总志愿者数
        total_volunteers_query = select(func.count(volunteer_profile.c.id))
        total_volunteers = await database.fetch_one(total_volunteers_query)

        # 统计总活动数
        total_activities_query = select(func.count(volunteer_plans.c.id))
        total_activities = await database.fetch_one(total_activities_query)

        # 统计总参与记录数
        total_participations_query = select(func.count(participation.c.id))
        total_participations = await database.fetch_one(total_participations_query)

        # 统计总服务时长
        total_hours_query = select(func.sum(participation.c.service_hours))
        total_hours = await database.fetch_one(total_hours_query)

        # 统计已完成活动数
        completed_activities_query = select(func.count(volunteer_plans.c.id)).where(
            volunteer_plans.c.status == "completed"
        )
        completed_activities = await database.fetch_one(completed_activities_query)

        # 统计进行中活动数
        ongoing_activities_query = select(func.count(volunteer_plans.c.id)).where(
            volunteer_plans.c.status == "ongoing"
        )
        ongoing_activities = await database.fetch_one(ongoing_activities_query)

        result = VolunteerStatistics(
            total_volunteers=total_volunteers.count_1 or 0,
            total_activities=total_activities.count_1 or 0,
            total_participations=total_participations.count_1 or 0,
            total_service_hours=float(total_hours.sum_1 or 0),
            completed_activities=completed_activities.count_1 or 0,
            ongoing_activities=ongoing_activities.count_1 or 0,
        )

        logger.info(f"志愿者统计成功：{result}")
        return result
    except Exception as err:
        logger.error(f"获取志愿者统计信息失败：{str(err)}")
        return VolunteerStatistics(
            total_volunteers=0,
            total_activities=0,
            total_participations=0,
            total_service_hours=0.0,
            completed_activities=0,
            ongoing_activities=0,
        )


async def get_activity_type_statistics(query: StatisticsQuery = None):
    """获取活动类型统计信息"""
    try:
        # 按活动类型统计
        type_stats_query = (
            select(
                volunteer_plans.c.activity_type,
                func.count(volunteer_plans.c.id).label("count"),
                func.sum(volunteer_plans.c.max_participants).label(
                    "total_participants"
                ),
                func.coalesce(func.sum(participation.c.service_hours), 0).label(
                    "total_service_hours"
                ),
            )
            .select_from(
                volunteer_plans.outerjoin(
                    participation, volunteer_plans.c.id == participation.c.activity_id
                )
            )
            .group_by(volunteer_plans.c.activity_type)
        )

        if query and query.start_date:
            type_stats_query = type_stats_query.where(
                volunteer_plans.c.activity_date >= query.start_date
            )
        if query and query.end_date:
            type_stats_query = type_stats_query.where(
                volunteer_plans.c.activity_date <= query.end_date
            )

        type_stats = await database.fetch_all(type_stats_query)

        return [
            ActivityStatistics(
                activity_type=stat.activity_type,
                count=int(stat.count) if stat.count else 0,
                total_participants=(
                    int(stat.total_participants) if stat.total_participants else 0
                ),
                total_service_hours=float(stat.total_service_hours or 0),
            )
            for stat in type_stats
        ]
    except Exception as err:
        print(err)
        return []


async def get_user_statistics(query: StatisticsQuery = None):
    """获取用户统计信息"""
    try:
        # 按用户统计参与活动和服务时长
        user_stats_query = select(
            participation.c.user_id,
            participation.c.user_name,
            func.count(participation.c.id).label("total_activities"),
            func.sum(participation.c.service_hours).label("total_service_hours"),
        ).group_by(participation.c.user_id, participation.c.user_name)

        if query and query.user_id:
            user_stats_query = user_stats_query.where(
                participation.c.user_id == query.user_id
            )
        if query and query.start_date:
            user_stats_query = user_stats_query.where(
                participation.c.activity_date >= query.start_date
            )
        if query and query.end_date:
            user_stats_query = user_stats_query.where(
                participation.c.activity_date <= query.end_date
            )

        user_stats = await database.fetch_all(user_stats_query)

        # 获取用户等级信息
        result = []
        for stat in user_stats:
            profile_query = select(volunteer_profile.c.volunteer_level).where(
                volunteer_profile.c.user_id == stat.user_id
            )
            profile = await database.fetch_one(profile_query)

            result.append(
                UserStatistics(
                    user_id=stat.user_id,
                    user_name=stat.user_name,
                    total_activities=stat.total_activities,
                    total_service_hours=float(stat.total_service_hours or 0),
                    volunteer_level=profile.volunteer_level if profile else "beginner",
                )
            )

        return result
    except Exception as err:
        print(err)
        return []


async def get_monthly_statistics(year: int, month: int):
    """获取月度统计信息"""
    try:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        # 月度活动统计
        monthly_activities_query = select(func.count(volunteer_plans.c.id)).where(
            and_(
                volunteer_plans.c.activity_date >= start_date,
                volunteer_plans.c.activity_date < end_date,
            )
        )
        monthly_activities = await database.fetch_one(monthly_activities_query)

        # 月度参与统计
        monthly_participations_query = select(func.count(participation.c.id)).where(
            and_(
                participation.c.activity_date >= start_date,
                participation.c.activity_date < end_date,
            )
        )
        monthly_participations = await database.fetch_one(monthly_participations_query)

        # 月度服务时长统计
        monthly_hours_query = select(func.sum(participation.c.service_hours)).where(
            and_(
                participation.c.activity_date >= start_date,
                participation.c.activity_date < end_date,
            )
        )
        monthly_hours = await database.fetch_one(monthly_hours_query)

        return {
            "year": year,
            "month": month,
            "total_activities": monthly_activities.count_1 or 0,
            "total_participations": monthly_participations.count_1 or 0,
            "total_service_hours": float(monthly_hours.sum_1 or 0),
        }
    except Exception as err:
        print(err)
        return {
            "year": year,
            "month": month,
            "total_activities": 0,
            "total_participations": 0,
            "total_service_hours": 0.0,
        }
