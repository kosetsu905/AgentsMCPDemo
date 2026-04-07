# mcp_servers/math_server.py
""" Example MCP server for math operations """

from fastmcp import FastMCP

# 创建MCP服务器实例
mcp = FastMCP("Math Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    # 以标准输入输出方式运行（便于集成）
    mcp.run(transport="stdio")