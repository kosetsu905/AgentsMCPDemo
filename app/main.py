# app/main.py
""" FastAPI application entry point """

import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.router import api_router
from app.core.config import settings
# from app.core.logging import setup_logging

# setup_logging()  # 初始化结构化日志
logger = structlog.get_logger(__name__)

# 生命周期管理：启动和关闭时的钩子
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_starting", environment=settings.ENVIRONMENT)
    yield # 应用运行中
    logger.info("application_shutting_down")

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI Agent with FastAPI, LangGraph, and MCP",
    version="0.1.0",
    lifespan=lifespan,  # 绑定生命周期管理
)

# 配置CORS（跨域资源共享）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载API路由
app.include_router(api_router, prefix="/api/v1")

# 健康检查端点
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={
            "status": "healthy",
            "environment": settings.ENVIRONMENT,
        }
    )

# 根端点
@app.get("/")
async def root():
    return {
        "message": "AI Agent API",
        "docs": "/docs",  # 自动生成的API文档
        "version": "0.1.0",
    }