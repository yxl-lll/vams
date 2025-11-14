#!/bin/bash

echo "=== 校园志愿者活动管理系统 - 容器启动脚本 ==="
echo ""

# 设置环境变量
export DB_HOST=${DB_HOST:-volunteer-db}
export DB_PORT=${DB_PORT:-3306}
export DB_USER=${DB_USER:-root}
export DB_PASSWORD=${DB_PASSWORD:-123456}
export DB_NAME=${DB_NAME:-volunteer}

echo "数据库配置:"
echo "  主机: $DB_HOST"
echo "  端口: $DB_PORT"
echo "  用户: $DB_USER"
echo "  数据库: $DB_NAME"
echo ""

# 等待数据库准备就绪
echo "等待数据库准备就绪..."
python3 wait_for_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo "数据库已就绪，启动应用..."
    echo ""
    
    # 启动应用
    exec python3 main.py
else
    echo ""
    echo "数据库连接失败，退出容器"
    exit 1
fi
