#!/usr/bin/env python3
"""
调试审核功能
"""
import requests
import json

def test_volunteer_plans_status():
    """测试活动计划状态更新API"""
    print("=== 测试活动计划状态更新API ===")
    
    # 测试数据
    test_data = {
        "status": "approved"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 使用一个测试ID
    test_id = "3cefaad5-9e77-43af-a9eb-268be821eb3d"
    
    try:
        response = requests.put(
            f"http://localhost:8000/volunteer_plans/status/{test_id}",
            headers=headers,
            json=test_data
        )
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 422:
            print("422错误 - 请求格式有问题")
            try:
                error_detail = response.json()
                print(f"错误详情: {error_detail}")
            except:
                print("无法解析错误响应")
        
        return response.status_code == 200
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_activity_audit_status():
    """测试活动审核状态更新API"""
    print("\n=== 测试活动审核状态更新API ===")
    
    # 测试数据
    test_data = {
        "status": "approved",
        "opinion": "测试审核通过"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 使用一个测试ID
    test_id = "test-audit-id"
    
    try:
        response = requests.put(
            f"http://localhost:8000/activity_audit/status/{test_id}",
            headers=headers,
            json=test_data
        )
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 422:
            print("422错误 - 请求格式有问题")
            try:
                error_detail = response.json()
                print(f"错误详情: {error_detail}")
            except:
                print("无法解析错误响应")
        
        return response.status_code == 200
    except Exception as e:
        print(f"请求失败: {e}")
        return False

if __name__ == "__main__":
    print("开始调试审核功能...")
    test_volunteer_plans_status()
    test_activity_audit_status()
