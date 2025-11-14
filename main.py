import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from config import database, global_config, h5config
from system import register_sys_router
from volunteer import register_volunteer_router
# 导入通知路由（仅用于重定向，挂载由 register_volunteer_router 统一处理）
from volunteer.notification.routes import notification_route

app = FastAPI()

# 核心：通知模块路径重定向（覆盖 GET/POST/DELETE/PUT 所有方法）
# app.add_api_route(
#    "/notification/{path:path}",
#   lambda path: RedirectResponse(f"/api/notification/{path}"),
#  methods=["GET", "POST", "DELETE", "PUT"]
# )

# 挂载静态文件（前端页面）
app.mount("/static", StaticFiles(directory=global_config["static"]), name="static")


# 数据库连接
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        # 测试数据库连接
        await database.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# 全局配置（H5相关）
h5config(app)

# 注册系统模块路由
register_sys_router(app)

# 注册志愿者模块路由（包含通知路由挂载）
register_volunteer_router(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
