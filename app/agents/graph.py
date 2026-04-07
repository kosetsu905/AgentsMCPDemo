# app/agents/graph.py
""" LangGraph agent definition """

import structlog
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from app.agents.state import AgentState
from app.agents.tools import get_tools
from app.services.llm import get_llm

logger = structlog.get_logger(__name__)


def create_agent_graph():
    """创建Agent工作流图"""
    # 1. 获取LLM和工具
    llm = get_llm()
    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)  # 让LLM知道它能使用哪些工具

    # 2. 创建状态图
    workflow = StateGraph(AgentState)

    # 3. 定义Agent节点（思考）
    async def call_model(state: AgentState) -> dict:
        """LLM推理节点：分析当前状态并决定下一步"""
        logger.info("calling_model")
        # LLM基于当前对话历史进行推理
        response = await llm_with_tools.ainvoke(state["messages"])
        return {"messages": [response]}  # 返回的消息会自动添加到状态中


    # 4. 定义工具节点（执行）
    tool_node = ToolNode(tools)  # 预建的ToolNode自动处理工具调用

    # 5. 添加节点到图中
    workflow.add_node("agent", call_model)  # 思考节点
    workflow.add_node("tools", tool_node)  # 执行节点

    # 6. 设置起始边
    workflow.add_edge(START, "agent")  # 从开始直接到agent思考


    # 7. 定义条件边：Agent思考后该做什么？
    def should_continue(state: AgentState) -> str:
        """判断是否需要调用工具"""
        last_message = state["messages"][-1]
        # 如果LLM返回了工具调用请求，则执行工具
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return END  # 否则结束


    # 8. 添加条件边
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        ["tools", END]  # 可能的两条路径
    )

    # 9. 工具执行后回到Agent继续思考
    workflow.add_edge("tools", "agent")

    # 10. 编译图为可执行对象
    return workflow.compile()

# Agent单例模式，避免重复创建
_agent = None


def get_agent():
    """获取Agent实例（单例）"""
    global _agent
    if _agent is None:
        _agent = create_agent_graph()
    return _agent


async def invoke_agent(query: str, session_id: str | None = None) -> dict:
    """调用Agent处理查询"""
    logger.info("invoking_agent", query=query)

    # 获取Agent实例
    agent = get_agent()

    # 初始化状态：用户消息作为起点
    initial_state = {"messages": [HumanMessage(content=query)]}

    # 执行Agent工作流
    result = await agent.ainvoke(initial_state)

    # 提取最终回复
    final_message = result["messages"][-1]
    response = {
        "response": final_message.content if isinstance(final_message, AIMessage) else str(final_message),
        "message_count": len(result["messages"]),  # 总共的消息轮数
        "session_id": session_id,  # 会话ID，支持多轮对话
    }

    return response