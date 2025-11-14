# 校园志愿者活动管理系统

## 项目简介

这是一个基于FastAPI框架开发的校园志愿者活动管理系统，旨在为高校提供完整的志愿者活动管理解决方案。

## 主要功能

### 🎯 核心功能模块

- **活动计划管理**: 创建、编辑、删除志愿者活动计划
- **活动类型管理**: 支持多种活动类型分类和难度等级
- **活动参与记录**: 志愿者报名、签到、签退和服务时长记录
- **活动审核管理**: 活动计划审核流程管理
- **志愿者档案**: 志愿者个人信息和服务统计
- **通知消息**: 活动通知和提醒功能
- **统计报表**: 服务时长统计和活动数据分析

### 🔐 系统管理

- **用户管理**: 用户注册、登录、权限管理
- **角色管理**: 基于RBAC的权限控制
- **菜单管理**: 动态菜单配置

## 技术架构

### 后端技术栈

- **框架**: FastAPI
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy
- **认证**: JWT Token
- **异步**: asyncio + aiomysql

### 前端技术栈

- **模板引擎**: Jinja2
- **UI框架**: LayUI
- **响应式**: 支持移动端和桌面端

## 快速开始

### 环境要求

- Python 3.10+
- MySQL 8.0+
- Docker & Docker Compose

### 使用Docker启动

1. 克隆项目
```bash
git clone <repository-url>
cd volunteer-management-system
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问系统
- 前端地址: http://localhost:8000
- 数据库端口: 13306

### 手动安装

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置数据库
- 创建数据库: `volunteer`
- 导入数据: `volunteer.sql`

3. 启动服务
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 数据库设计

### 核心表结构

- `volunteer_plans`: 志愿者活动计划
- `participation`: 活动参与记录
- `activity_type`: 活动类型分类
- `activity_audit`: 活动审核记录
- `volunteer_profile`: 志愿者档案
- `notification`: 通知消息
- `service_hours`: 服务时长记录

## API文档

启动服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 功能特性

### ✨ 志愿者活动管理

- 支持多种活动类型（社区服务、环保、教育、医疗等）
- 活动计划创建和编辑
- 活动状态管理（草稿、待审核、已通过、进行中、已完成等）
- 参与人数限制和报名管理

### ⏰ 服务时长系统

- 自动计算服务时长
- 签到签退记录
- 累计服务时长统计
- 个人服务报表

### 🔍 审核流程

- 活动计划审核
- 审核意见记录
- 审核状态跟踪
- 权限分级管理

### 📊 数据统计

- 志愿者服务时长统计
- 活动参与情况分析
- 部门/学院活动统计
- 月度/年度报表生成

## 开发说明

### 项目结构

```
volunteer-management-system/
├── config/                 # 配置文件
├── system/                 # 系统管理模块
├── volunteer/              # 志愿者活动模块
│   ├── volunteer_plans/    # 活动计划管理
│   ├── participation/      # 活动参与记录
│   ├── activity_type/      # 活动类型管理
│   ├── activity_audit/     # 活动审核管理
│   ├── volunteer_profile/  # 志愿者档案
│   ├── notification/       # 通知消息
│   └── statistics/         # 统计报表
├── utils/                  # 工具模块
├── web/                    # 前端模板和静态资源
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── docker-compose.yml      # Docker编排文件
└── volunteer.sql           # 数据库初始化脚本
```

### 开发规范

- 使用Python类型注解
- 异步编程模式
- RESTful API设计
- 统一的响应格式
- 完整的错误处理

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 项目讨论区
