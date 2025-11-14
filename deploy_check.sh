#!/bin/bash

echo "=== 校园志愿者活动管理系统 - 部署验证脚本 ==="
echo ""

# 检查Docker服务状态
echo "🔍 检查Docker服务状态..."
if systemctl is-active --quiet docker; then
    echo "✅ Docker服务正在运行"
else
    echo "❌ Docker服务未运行，请启动Docker"
    exit 1
fi

# 检查Docker Compose
echo ""
echo "🔍 检查Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose已安装"
else
    echo "❌ Docker Compose未安装，请先安装"
    exit 1
fi

# 检查项目文件
echo ""
echo "🔍 检查项目文件..."
required_files=("main.py" "config.yml" "volunteer.sql" "requirements.txt" "docker-compose.yml")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
    fi
done

# 检查项目目录
echo ""
echo "🔍 检查项目目录..."
required_dirs=("config" "system" "volunteer" "utils" "web")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ 目录存在"
    else
        echo "❌ $dir/ 目录缺失"
    fi
done

# 检查容器状态
echo ""
echo "🔍 检查容器状态..."
if [ -f "docker-compose.yml" ]; then
    echo "📊 当前容器状态:"
    docker-compose ps
    
    echo ""
    echo "📋 容器日志检查:"
    echo "数据库容器日志:"
    docker-compose logs --tail=5 volunteer-db
    
    echo ""
    echo "Web应用容器日志:"
    docker-compose logs --tail=5 volunteer-web
else
    echo "❌ docker-compose.yml 文件不存在"
fi

# 检查端口占用
echo ""
echo "🔍 检查端口占用..."
echo "端口8000 (Web应用):"
if netstat -tuln | grep :8000 > /dev/null; then
    echo "✅ 端口8000正在监听"
else
    echo "❌ 端口8000未监听"
fi

echo "端口13306 (数据库):"
if netstat -tuln | grep :13306 > /dev/null; then
    echo "✅ 端口13306正在监听"
else
    echo "❌ 端口13306未监听"
fi

# 检查网络连接
echo ""
echo "🔍 检查网络连接..."
echo "测试本地Web应用连接:"
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ Web应用可以访问"
else
    echo "❌ Web应用无法访问"
fi

echo ""
echo "=== 部署验证完成 ==="
echo ""
echo "如果发现问题，请检查:"
echo "1. Docker服务是否正常运行"
echo "2. 容器是否正常启动"
echo "3. 端口是否被占用"
echo "4. 配置文件是否正确"
echo ""
echo "使用以下命令查看详细日志:"
echo "  docker-compose logs -f"
echo "  docker-compose logs volunteer-db"
echo "  docker-compose logs volunteer-web"
