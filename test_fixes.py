#!/usr/bin/env python3
"""
测试修复后的功能
"""
import json
from datetime import datetime

import requests

# 测试配置
BASE_URL = "http://localhost:8000"
AUTH_TOKEN = "your_auth_token_here"  # 需要替换为实际的认证token


def test_participation_add():
    """测试报名活动功能"""
    print("=== 测试报名活动功能 ===")

    # 测试数据
    test_data = {
        "activity_id": "test-activity-id",
        "activity_name": "测试活动",
        "activity_image": None,
        "activity_date": datetime.now().isoformat(),
        "activity_type": "志愿服务",
        "service_hours": 2.0,
        "participant_count": 1,
        "remark": "测试报名",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/participation/add", headers=headers, json=test_data
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"请求失败: {e}")
        return False


def test_activity_audit_status():
    """测试活动审核功能"""
    print("\n=== 测试活动审核功能 ===")

    # 测试数据
    test_data = {"status": "approved", "opinion": "测试审核通过"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}",
    }

    try:
        response = requests.put(
            f"{BASE_URL}/activity_audit/status/test-audit-id",
            headers=headers,
            json=test_data,
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"请求失败: {e}")
        return False


def test_volunteer_plans_status():
    """测试活动计划状态更新"""
    print("\n=== 测试活动计划状态更新 ===")

    # 测试数据
    test_data = {"status": "approved"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}",
    }

    try:
        response = requests.put(
            f"{BASE_URL}/volunteer_plans/status/test-plan-id",
            headers=headers,
            json=test_data,
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"请求失败: {e}")
        return False


def main():
    print("开始测试修复后的功能...")
    print("注意：需要先启动服务器并获取有效的认证token")

    # 测试报名功能
    participation_ok = test_participation_add()

    # 测试审核功能
    audit_ok = test_activity_audit_status()

    # 测试活动计划状态更新
    plans_ok = test_volunteer_plans_status()

    print(f"\n=== 测试结果 ===")
    print(f"报名活动: {'✓ 通过' if participation_ok else '✗ 失败'}")
    print(f"活动审核: {'✓ 通过' if audit_ok else '✗ 失败'}")
    print(f"活动计划状态更新: {'✓ 通过' if plans_ok else '✗ 失败'}")


if __name__ == "__main__":
    main()
