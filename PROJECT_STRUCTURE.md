# 校园志愿者活动管理系统 - 项目结构说明

## 📁 项目目录结构

```
volunteer-management-system/
├── config/                     # 配置文件目录
│   ├── __init__.py            # 配置模块初始化
│   ├── config.py              # 主配置文件
│   └── h5_config.py           # H5配置和中间件
├── system/                     # 系统管理模块
│   ├── __init__.py            # 系统模块初始化
│   ├── register_router.py     # 系统路由注册
│   ├── user/                  # 用户管理
│   ├── role/                  # 角色管理
│   ├── menu/                  # 菜单管理
│   └── login/                 # 登录认证
├── volunteer/                  # 志愿者活动模块
│   ├── __init__.py            # 志愿者模块初始化
│   ├── register_router.py     # 志愿者路由注册
│   ├── volunteer_plans/       # 活动计划管理
│   ├── participation/         # 活动参与记录
│   ├── activity_type/         # 活动类型管理
│   ├── activity_audit/        # 活动审核管理
│   ├── volunteer_profile/     # 志愿者档案
│   ├── notification/          # 通知消息
│   └── statistics/            # 统计报表
├── utils/                      # 工具模块
│   ├── depends.py             # 依赖注入和认证
│   ├── fix_query.py           # 查询构建工具
│   ├── passwd.py              # 密码处理工具
│   └── result.py              # 统一响应格式
├── web/                        # 前端资源
│   ├── static/                # 静态资源
│   │   ├── layui/             # LayUI框架
│   │   ├── style/             # 自定义样式
│   │   └── views/             # 前端页面
│   │       ├── home/          # 首页
│   │       ├── volunteer-plans/ # 活动计划管理
│   │       ├── participation/   # 活动参与记录
│   │       ├── activity-type/   # 活动类型管理
│   │       └── statistics/      # 统计报表
│   └── templates/             # 后端模板
│       ├── index.html         # 主页面
│       ├── login.html         # 登录页面
│       └── register.html      # 注册页面
├── main.py                     # 主程序入口
├── requirements.txt            # Python依赖包
├── volunteer.sql               # 数据库初始化脚本
├── docker-compose.yml          # Docker编排配置
├── Dockerfile                  # Docker镜像构建
├── start.sh                    # 系统启动脚本
├── README.md                   # 项目说明文档
└── PROJECT_STRUCTURE.md        # 项目结构说明
```

## 🔧 核心模块说明

### 1. 配置模块 (config/)
- **config.py**: 数据库连接、模板配置、全局配置
- **h5_config.py**: HTTP中间件、认证重定向

### 2. 系统管理模块 (system/)
- **用户管理**: 用户CRUD、角色分配、权限控制
- **角色管理**: 基于RBAC的权限体系
- **菜单管理**: 动态菜单配置、权限控制
- **登录认证**: JWT Token认证、会话管理

### 3. 志愿者活动模块 (volunteer/)
- **活动计划管理**: 创建、编辑、删除活动计划
- **活动参与记录**: 报名、签到、签退、时长统计
- **活动类型管理**: 活动分类、难度等级、技能要求
- **活动审核管理**: 计划审核、审核流程
- **志愿者档案**: 个人信息、服务统计、技能标签
- **通知消息**: 活动通知、系统公告、提醒功能
- **统计报表**: 服务时长统计、活动数据分析

### 4. 工具模块 (utils/)
- **depends.py**: FastAPI依赖注入、JWT认证
- **fix_query.py**: 动态查询构建、条件过滤
- **passwd.py**: 密码加密、RSA加解密
- **result.py**: 统一API响应格式、数据编码

## 🌐 前端页面说明

### 1. 主页面 (index.html)
- 系统导航菜单
- 功能模块快捷入口
- 用户信息显示

### 2. 登录页面 (login.html)
- 用户登录表单
- 现代化UI设计
- 响应式布局

### 3. 注册页面 (register.html)
- 用户注册表单
- 完整信息收集
- 表单验证

### 4. 功能页面
- **活动计划管理**: 列表、新增、编辑、删除
- **活动参与记录**: 记录管理、签到签退
- **活动类型管理**: 类型CRUD、分类管理
- **统计报表**: 数据可视化、报表导出

## 🚀 部署说明

### 1. Docker部署 (推荐)
```bash
# 启动系统
./start.sh

# 手动启动
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 2. 手动部署
```bash
# 安装依赖
pip install -r requirements.txt

# 配置数据库
mysql -u root -p < volunteer.sql

# 启动服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 数据库设计

### 核心数据表
- `volunteer_plans`: 志愿者活动计划
- `participation`: 活动参与记录
- `activity_type`: 活动类型分类
- `activity_audit`: 活动审核记录
- `volunteer_profile`: 志愿者档案
- `notification`: 通知消息
- `service_hours`: 服务时长记录

### 系统管理表
- `user`: 用户信息
- `role`: 角色定义
- `menu`: 菜单配置
- `user_role`: 用户角色关联
- `menu_role`: 菜单角色关联

## 🔐 权限体系

### 角色类型
- **管理员**: 系统管理、用户管理、活动审核
- **活动组织者**: 活动创建、报名管理、时长记录
- **普通志愿者**: 活动报名、参与记录、个人统计

### 权限控制
- 基于角色的访问控制(RBAC)
- 菜单级权限控制
- API接口权限验证
- 数据级权限隔离

## 📈 功能特性

### 1. 活动管理
- 活动计划创建和编辑
- 活动状态全生命周期管理
- 参与人数限制和报名管理
- 活动审核流程

### 2. 时长统计
- 自动计算服务时长
- 累计时长统计
- 个人服务报表
- 组织活动统计

### 3. 通知系统
- 活动开始提醒
- 报名成功通知
- 系统公告发布
- 消息状态跟踪

### 4. 数据统计
- 志愿者服务统计
- 活动参与分析
- 部门/学院统计
- 月度/年度报表

## 🛠️ 开发规范

### 代码规范
- Python类型注解
- 异步编程模式
- RESTful API设计
- 统一错误处理

### 架构原则
- 模块化设计
- 依赖注入
- 分层架构
- 配置外部化
