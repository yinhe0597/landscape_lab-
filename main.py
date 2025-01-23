# landscape_lab/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from landscape_lab.database.db import init_db
from controllers import (
    user_controller,
    plant_controller,
    material_controller,
    project_controller
)

# 创建FastAPI应用
app = FastAPI(
    title="风景园林实训室数据管理系统",
    description="用于管理风景园林专业实训室的数据模块",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    await init_db()

# 注册路由
app.include_router(user_controller.router, prefix="/api/users", tags=["用户管理"])
app.include_router(plant_controller.router, prefix="/api/plants", tags=["植物管理"])
app.include_router(material_controller.router, prefix="/api/materials", tags=["材料管理"])
app.include_router(project_controller.router, prefix="/api/projects", tags=["项目管理"])

if __name__ == "__main__":
    # 启动开发服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
