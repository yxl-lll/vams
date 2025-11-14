# 校园志愿者活动管理系统
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 使用阿里云的 Ubuntu 镜像源（国内加速）
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 更新包列表并安装必要的软件
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    mysql-client \
    netcat \
    curl \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 使用清华源安装 Python 依赖（国内加速）
RUN pip3 install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

# 单独安装 mysql-connector-python（可选：也可包含在 requirements.txt 中）
RUN pip3 install --no-cache-dir mysql-connector-python \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs /app/uploads

# 设置权限（只对存在的文件）
RUN if [ -f "docker-entrypoint.sh" ]; then chmod +x docker-entrypoint.sh; fi

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 使用启动脚本
ENTRYPOINT ["./docker-entrypoint.sh"]