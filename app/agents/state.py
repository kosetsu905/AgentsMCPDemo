# app/agents/state.py
""" Agent state definition """

from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages  # 关键：自动消息累加

class AgentState(TypedDict):
    # 使用Annotated标注特殊处理逻辑
    messages: Annotated[list[BaseMessage], add_messages]