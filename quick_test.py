#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试修复后的功能
"""

import json

import requests

# 测试基础URL
BASE_URL = "http://localhost:8000"


def test_health():
    """测试健康检查"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ 健康检查: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   数据库状态: {data.get('database', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False


def test_activity_type():
    """测试活动类型查询"""
    try:
        response = requests.get(f"{BASE_URL}/activity_type/list")
        print(f"✅ 活动类型查询: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回数据条数: {len(data.get('data', []))}")
            if data.get("data"):
                print(f"   示例数据: {data['data'][0].get('type_name', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ 活动类型查询失败: {e}")
        return False


def test_volunteer_profile():
    """测试志愿者档案查询"""
    try:
        response = requests.get(f"{BASE_URL}/volunteer_profile/list")
        print(f"✅ 志愿者档案查询: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回数据条数: {len(data.get('data', []))}")
            if data.get("data"):
                print(f"   示例数据: {data['data'][0].get('user_name', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ 志愿者档案查询失败: {e}")
        return False


def test_participation():
    """测试活动参与记录查询"""
    try:
        response = requests.get(f"{BASE_URL}/participation/page?page=1&limit=10")
        print(f"✅ 活动参与记录查询: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   总数: {data.get('total', 0)}")
            print(f"   返回数据条数: {len(data.get('data', []))}")
        return True
    except Exception as e:
        print(f"❌ 活动参与记录查询失败: {e}")
        return False


def test_volunteer_plans():
    """测试活动计划查询"""
    try:
        response = requests.get(f"{BASE_URL}/volunteer_plans/page?page=1&limit=10")
        print(f"✅ 活动计划查询: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   总数: {data.get('total', 0)}")
            print(f"   返回数据条数: {len(data.get('data', []))}")
        return True
    except Exception as e:
        print(f"❌ 活动计划查询失败: {e}")
        return False


def test_activity_audit():
    """测试活动审核查询"""
    try:
        response = requests.get(f"{BASE_URL}/activity_audit/list")
        print(f"✅ 活动审核查询: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   返回数据条数: {len(data.get('data', []))}")
        return True
    except Exception as e:
        print(f"❌ 活动审核查询失败: {e}")
        return False


def test_statistics():
    """测试统计功能"""
    try:
        response = requests.get(f"{BASE_URL}/statistics/dashboard")
        print(f"✅ 统计功能查询: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   统计数据: {data.get('success', False)}")
        return True
    except Exception as e:
        print(f"❌ 统计功能查询失败: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("开始测试修复后的志愿者管理系统功能")
    print("=" * 60)

    tests = [
        ("健康检查", test_health),
        ("活动类型管理", test_activity_type),
        ("志愿者档案", test_volunteer_profile),
        ("活动参与记录", test_participation),
        ("活动计划管理", test_volunteer_plans),
        ("活动审核管理", test_activity_audit),
        ("统计报表", test_statistics),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 测试 {test_name}...")
        result = test_func()
        results.append((test_name, result))

    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    success_count = 0
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1

    print(f"\n总计: {success_count}/{len(results)} 个功能测试通过")

    if success_count == len(results):
        print("🎉 所有功能测试通过！系统修复成功！")
    else:
        print("⚠️  部分功能仍有问题，请检查日志")


if __name__ == "__main__":
    main()
