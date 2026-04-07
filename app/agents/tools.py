# app/agents/tools.py
""" Custom tools for the agent """

import structlog
from typing import List
from langchain_core.tools import tool  # 关键装饰器
from datetime import datetime

logger = structlog.get_logger(__name__)

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression"""
    try:
        # 安全地计算数学表达式
        result = eval(expression, {"__builtins__": {}})
        logger.info("calculator_used", expression=expression, result=result)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_current_time() -> str:
    """Get the current time in ISO format"""
    return datetime.now().isoformat()

def get_tools() -> List:
    """获取所有可用工具"""
    return [calculator, get_current_time]