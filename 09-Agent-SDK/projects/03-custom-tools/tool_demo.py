#!/usr/bin/env python3
"""
自定义工具 Agent —— 用 @tool 装饰器给 Agent 添加新能力

演示:
  - @tool 装饰器定义自定义工具
  - create_sdk_mcp_server 创建工具服务器
  - 将自定义工具注入 Agent
  - Agent 自动选择并调用合适的工具

运行: python tool_demo.py
"""

import asyncio
import json
from datetime import datetime

from claude_code_sdk import (
    query, ClaudeCodeOptions,
    tool, create_sdk_mcp_server,
    AssistantMessage, ResultMessage, TextBlock, ToolUseBlock,
)


# ── 定义自定义工具 ──────────────────────────────────

@tool("get_time", "获取当前日期和时间", {"timezone": str})
async def get_time(args: dict) -> dict:
    """返回当前时间"""
    now = datetime.now()
    return {
        "content": [
            {"type": "text", "text": now.strftime("%Y-%m-%d %H:%M:%S")}
        ]
    }


@tool("calculate", "计算数学表达式，如 2+3*4", {"expression": str})
async def calculate(args: dict) -> dict:
    """安全计算数学表达式"""
    expr = args["expression"]
    # 只允许数字和基本运算符
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expr):
        return {
            "content": [{"type": "text", "text": f"不安全的表达式: {expr}"}],
            "isError": True,
        }
    try:
        result = eval(expr)  # 已过滤，仅含数字和运算符
        return {
            "content": [{"type": "text", "text": f"{expr} = {result}"}]
        }
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"计算错误: {e}"}],
            "isError": True,
        }


@tool(
    "lookup_city",
    "查询城市的基本信息（人口、国家、特色）",
    {"city": str},
)
async def lookup_city(args: dict) -> dict:
    """查询城市信息（模拟数据）"""
    db = {
        "新加坡": {"country": "新加坡", "population": "5.9M", "feature": "花园城市"},
        "东京": {"country": "日本", "population": "14M", "feature": "全球最大都市圈"},
        "上海": {"country": "中国", "population": "24.9M", "feature": "国际金融中心"},
    }
    city = args["city"]
    info = db.get(city)
    if info:
        text = f"{city} — {info['country']}，人口 {info['population']}，{info['feature']}"
    else:
        text = f"未找到城市: {city}"
    return {"content": [{"type": "text", "text": text}]}


# ── 创建 MCP 工具服务器 ──────────────────────────────

tools_server = create_sdk_mcp_server(
    name="demo-tools",
    version="1.0.0",
    tools=[get_time, calculate, lookup_city],
)


# ── 调用 Agent ────────────────────────────────────────

async def main():
    options = ClaudeCodeOptions(
        max_turns=5,
        mcp_servers={"demo": tools_server},
        allowed_tools=[
            "mcp__demo__get_time",
            "mcp__demo__calculate",
            "mcp__demo__lookup_city",
        ],
    )

    prompt = """请完成以下三个任务：
1. 告诉我现在几点
2. 计算 (12 + 8) * 3.5
3. 查一下新加坡的信息

每个任务用对应的工具完成，最后汇总结果。"""

    print("🤖 Agent 开始工作...\n")

    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
                    elif isinstance(block, ToolUseBlock):
                        print(f"  🔧 调用工具: {block.name}({json.dumps(block.input, ensure_ascii=False)})")

            elif isinstance(msg, ResultMessage):
                print(f"\n--- 统计 ---")
                print(f"轮次: {msg.num_turns} | 费用: ${msg.total_cost_usd:.4f}")

    except Exception as e:
        if "Unknown message type" not in str(e):
            raise


asyncio.run(main())
