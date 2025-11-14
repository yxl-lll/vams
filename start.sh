#!/bin/bash

echo "=== 校园志愿者活动管理系统启动脚本 ==="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "正在启动系统..."

# 停止并删除现有容器
echo "清理现有容器..."
docker-compose down

# 清理旧镜像（可选）
echo "清理旧镜像..."
docker-compose down --rmi all --volumes --remove-orphans

# 构建新镜像
echo "构建新镜像..."
docker-compose build --no-cache

# 启动服务
echo "启动服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 15

# 检查服务状态
echo "检查服务状态..."
docker-compose ps

# 检查数据库健康状态
echo ""
echo "检查数据库健康状态..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker-compose exec -T volunteer-db mysqladmin ping -h localhost -u root -p123456 > /dev/null 2>&1; then
        echo "✅ 数据库已就绪"
        break
    else
        echo "⏳ 等待数据库就绪... (第 $attempt/$max_attempts 次)"
        sleep 5
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ 数据库启动超时"
    echo "查看数据库日志:"
    docker-compose logs volunteer-db
    exit 1
fi

# 检查Web应用状态
echo ""
echo "检查Web应用状态..."
max_attempts=20
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Web应用已就绪"
        break
    else
        echo "⏳ 等待Web应用就绪... (第 $attempt/$max_attempts 次)"
        sleep 5
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Web应用启动超时"
    echo "查看Web应用日志:"
    docker-compose logs volunteer-web
    exit 1
fi

echo ""
echo "=== 系统启动完成 ==="
echo "访问地址: http://localhost:8000"
echo "数据库端口: 13306"
echo "健康检查: http://localhost:8000/health"
echo ""
echo "使用以下命令查看日志:"
echo "  docker-compose logs -f"
echo "  docker-compose logs -f volunteer-web"
echo "  docker-compose logs -f volunteer-db"
echo ""
echo "使用以下命令停止服务:"
echo "  docker-compose down"
echo ""
echo "使用以下命令重启服务:"
echo "  docker-compose restart"
