from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.user_controller import router as user_router
from views.user_view import router as user_view_router
from database.db import Base, engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Landscape Lab API",
    description="风景园林专业实训室软件数据模块API",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(user_router, prefix="/api/v1")
app.include_router(user_view_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Landscape Lab API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
