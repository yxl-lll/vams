#!/usr/bin/env python3
"""
测试修复后的API接口
验证total字段是否正确返回
"""

import json

import requests

# 基础URL
BASE_URL = "http://192.168.154.130:8000"


def test_activity_type_list():
    """测试活动类型列表接口"""
    print("🔍 测试活动类型列表接口...")

    try:
        response = requests.get(f"{BASE_URL}/activity_type/list")
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            # 检查关键字段
            if "count" in data and "data" in data:
                print(f"✅ count字段: {data['count']}")
                print(f"✅ data数组长度: {len(data['data'])}")

                if data["count"] == len(data["data"]) and data["count"] > 0:
                    print("🎉 修复成功！count字段等于实际数据条数")
                else:
                    print("❌ 修复失败！count字段不等于实际数据条数")
            else:
                print("❌ 响应中缺少count或data字段")
        else:
            print(f"❌ 请求失败: {response.text}")

    except Exception as e:
        print(f"❌ 测试异常: {e}")


def test_volunteer_profile_list():
    """测试志愿者档案列表接口"""
    print("\n🔍 测试志愿者档案列表接口...")

    try:
        response = requests.get(f"{BASE_URL}/volunteer_profile/list")
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if "count" in data and "data" in data:
                print(f"✅ count字段: {data['count']}")
                print(f"✅ data数组长度: {len(data['data'])}")

                if data["count"] == len(data["data"]):
                    print("🎉 修复成功！count字段等于实际数据条数")
                else:
                    print("❌ 修复失败！count字段不等于实际数据条数")
            else:
                print("❌ 响应中缺少count或data字段")
        else:
            print(f"❌ 请求失败: {response.text}")

    except Exception as e:
        print(f"❌ 测试异常: {e}")


def test_activity_audit_list():
    """测试活动审核列表接口"""
    print("\n🔍 测试活动审核列表接口...")

    try:
        response = requests.get(f"{BASE_URL}/activity_audit/list")
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if "count" in data and "data" in data:
                print(f"✅ count字段: {data['count']}")
                print(f"✅ data数组长度: {len(data['data'])}")

                if data["count"] == len(data["data"]):
                    print("🎉 修复成功！count字段等于实际数据条数")
                else:
                    print("❌ 修复失败！count字段不等于实际数据条数")
            else:
                print("❌ 响应中缺少count或data字段")
        else:
            print(f"❌ 请求失败: {response.text}")

    except Exception as e:
        print(f"❌ 测试异常: {e}")


if __name__ == "__main__":
    print("🚀 开始测试修复后的API接口...")
    print("=" * 50)

    # 测试各个接口
    test_activity_type_list()
    test_volunteer_profile_list()
    test_activity_audit_list()

    print("\n" + "=" * 50)
    print("🏁 测试完成！")
