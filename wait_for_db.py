#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库等待脚本
等待MySQL数据库准备就绪后再启动应用
"""

import os
import sys
import time
from datetime import datetime

import mysql.connector


def wait_for_mysql(host, port, user, password, database, max_attempts=60, delay=5):
    """
    等待MySQL数据库准备就绪

    Args:
        host: 数据库主机
        port: 数据库端口
        user: 用户名
        password: 密码
        database: 数据库名
        max_attempts: 最大尝试次数
        delay: 每次尝试间隔（秒）
    """
    print(f"[{datetime.now()}] 开始等待数据库 {host}:{port}/{database} 准备就绪...")

    for attempt in range(1, max_attempts + 1):
        try:
            print(
                f"[{datetime.now()}] 尝试连接数据库 (第 {attempt}/{max_attempts} 次)..."
            )

            # 尝试连接数据库
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                connection_timeout=10,
            )

            # 测试数据库连接
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result and result[0] == 1:
                print(f"[{datetime.now()}] ✅ 数据库连接成功！")
                return True

        except mysql.connector.Error as e:
            print(
                f"[{datetime.now()}] ❌ 数据库连接失败 (第 {attempt}/{max_attempts} 次): {e}"
            )

            if attempt < max_attempts:
                print(f"[{datetime.now()}] 等待 {delay} 秒后重试...")
                time.sleep(delay)
            else:
                print(f"[{datetime.now()}] ❌ 达到最大尝试次数，数据库连接失败")
                return False

    return False


def main():
    """主函数"""
    # 从环境变量获取数据库配置
    db_host = os.getenv("DB_HOST", "volunteer-db")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "123456")
    db_name = os.getenv("DB_NAME", "volunteer")

    # 等待数据库准备就绪
    if wait_for_mysql(db_host, db_port, db_user, db_password, db_name):
        print(f"[{datetime.now()}] 🎉 数据库准备就绪，可以启动应用了！")
        sys.exit(0)
    else:
        print(f"[{datetime.now()}] 💥 数据库连接失败，退出程序")
        sys.exit(1)


if __name__ == "__main__":
    main()
