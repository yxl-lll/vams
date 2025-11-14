#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校园志愿者活动管理系统 - 系统监控脚本
监控系统性能、资源使用和健康状态
"""

import json
import time
from datetime import datetime

import mysql.connector
import psutil

from config import global_config


class SystemMonitor:
    def __init__(self):
        self.db_config = self.parse_db_url(global_config["db"])

    def parse_db_url(self, db_url):
        """解析数据库连接URL"""
        # 格式: mysql://root:123456@localhost:3306/volunteer?charset=utf8
        try:
            parts = db_url.replace("mysql://", "").split("@")
            user_pass = parts[0].split(":")
            host_db = parts[1].split("/")
            host_port = host_db[0].split(":")

            return {
                "host": host_port[0],
                "port": int(host_port[1]) if len(host_port) > 1 else 3306,
                "user": user_pass[0],
                "password": user_pass[1],
                "database": host_db[1].split("?")[0],
            }
        except Exception as e:
            print(f"数据库URL解析失败: {e}")
            return None

    def get_system_info(self):
        """获取系统基本信息"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used": memory.used,
                "memory_total": memory.total,
                "disk_percent": disk.percent,
                "disk_used": disk.used,
                "disk_total": disk.total,
            }
        except Exception as e:
            print(f"获取系统信息失败: {e}")
            return None

    def get_database_info(self):
        """获取数据库信息"""
        if not self.db_config:
            return None

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()

            # 获取数据库状态
            cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
            threads_connected = cursor.fetchone()[1]

            cursor.execute("SHOW STATUS LIKE 'Queries'")
            queries = cursor.fetchone()[1]

            cursor.execute("SHOW STATUS LIKE 'Slow_queries'")
            slow_queries = cursor.fetchone()[1]

            cursor.execute("SHOW STATUS LIKE 'Uptime'")
            uptime = cursor.fetchone()[1]

            cursor.close()
            conn.close()

            return {
                "threads_connected": int(threads_connected),
                "queries": int(queries),
                "slow_queries": int(slow_queries),
                "uptime": int(uptime),
            }
        except Exception as e:
            print(f"获取数据库信息失败: {e}")
            return None

    def get_process_info(self):
        """获取进程信息"""
        try:
            processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent"]
            ):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # 按CPU使用率排序
            processes.sort(key=lambda x: x["cpu_percent"] or 0, reverse=True)

            return processes[:10]  # 返回前10个进程
        except Exception as e:
            print(f"获取进程信息失败: {e}")
            return []

    def check_system_health(self):
        """检查系统健康状态"""
        system_info = self.get_system_info()
        db_info = self.get_database_info()

        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "warnings": [],
            "errors": [],
        }

        if system_info:
            # CPU使用率检查
            if system_info["cpu_percent"] > 80:
                health_status["warnings"].append(
                    f"CPU使用率过高: {system_info['cpu_percent']}%"
                )
                health_status["overall_status"] = "warning"

            # 内存使用率检查
            if system_info["memory_percent"] > 85:
                health_status["warnings"].append(
                    f"内存使用率过高: {system_info['memory_percent']}%"
                )
                health_status["overall_status"] = "warning"

            # 磁盘使用率检查
            if system_info["disk_percent"] > 90:
                health_status["errors"].append(
                    f"磁盘使用率过高: {system_info['disk_percent']}%"
                )
                health_status["overall_status"] = "error"

        if db_info:
            # 数据库连接数检查
            if db_info["threads_connected"] > 100:
                health_status["warnings"].append(
                    f"数据库连接数过多: {db_info['threads_connected']}"
                )
                health_status["overall_status"] = "warning"

            # 慢查询检查
            if db_info["slow_queries"] > 10:
                health_status["warnings"].append(
                    f"慢查询数量较多: {db_info['slow_queries']}"
                )
                health_status["overall_status"] = "warning"

        return health_status

    def generate_report(self):
        """生成监控报告"""
        report = {
            "system_info": self.get_system_info(),
            "database_info": self.get_database_info(),
            "process_info": self.get_process_info(),
            "health_status": self.check_system_health(),
        }

        return report

    def save_report(self, report, filename=None):
        """保存监控报告"""
        if not filename:
            filename = f"system_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"监控报告已保存到: {filename}")
        except Exception as e:
            print(f"保存监控报告失败: {e}")

    def print_report(self, report):
        """打印监控报告"""
        print("=" * 60)
        print("校园志愿者活动管理系统 - 系统监控报告")
        print("=" * 60)

        # 系统信息
        if report["system_info"]:
            print("\n📊 系统信息:")
            print(f"  CPU使用率: {report['system_info']['cpu_percent']}%")
            print(f"  内存使用率: {report['system_info']['memory_percent']}%")
            print(f"  磁盘使用率: {report['system_info']['disk_percent']}%")

        # 数据库信息
        if report["database_info"]:
            print("\n🗄️  数据库信息:")
            print(f"  当前连接数: {report['database_info']['threads_connected']}")
            print(f"  总查询数: {report['database_info']['queries']}")
            print(f"  慢查询数: {report['database_info']['slow_queries']}")
            print(f"  运行时间: {report['database_info']['uptime']} 秒")

        # 健康状态
        health = report["health_status"]
        print(f"\n🏥 系统健康状态: {health['overall_status'].upper()}")

        if health["warnings"]:
            print("  ⚠️  警告:")
            for warning in health["warnings"]:
                print(f"    - {warning}")

        if health["errors"]:
            print("  ❌ 错误:")
            for error in health["errors"]:
                print(f"    - {error}")

        if not health["warnings"] and not health["errors"]:
            print("  ✅ 系统运行正常")

        print("\n" + "=" * 60)


def main():
    """主函数"""
    monitor = SystemMonitor()

    print("🔍 开始系统监控...")

    # 生成监控报告
    report = monitor.generate_report()

    # 打印报告
    monitor.print_report(report)

    # 保存报告
    monitor.save_report(report)

    print("✅ 系统监控完成")


if __name__ == "__main__":
    main()
