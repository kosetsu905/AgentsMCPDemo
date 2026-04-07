# app/api/v1/agent.py
""" Agent API endpoints """

import structlog
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.agents.graph import invoke_agent

logger = structlog.get_logger(__name__)
router = APIRouter()


# 请求模型（Pydantic验证）
class AgentRequest(BaseModel):
    query: str = Field(..., min_length=1, description="用户查询")
    session_id: str | None = Field(None, description="会话ID（用于多轮对话）")


# 响应模型
class AgentResponse(BaseModel):
    response: str = Field(..., description="Agent回复")
    message_count: int = Field(..., description="总消息轮数")
    session_id: str | None = Field(None, description="会话ID")


@router.post("/invoke", response_model=AgentResponse)


async def invoke_agent_endpoint(request: AgentRequest) -> AgentResponse:
    """调用Agent处理查询"""
    try:
        logger.info("agent_invoked", query=request.query)
        result = await invoke_agent(request.query, request.session_id)
        return AgentResponse(**result)
    except Exception as e:
        logger.error("agent_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")


async def agent_status():
    """获取Agent状态"""
    from app.core.config import settings
    from app.agents.tools import get_tools

    tools = get_tools()
    return {
        "status": "operational",
        "llm_provider": settings.LLM_PROVIDER,
        "tool_count": len(tools),
        "available_tools": [tool.name for tool in tools],
    }