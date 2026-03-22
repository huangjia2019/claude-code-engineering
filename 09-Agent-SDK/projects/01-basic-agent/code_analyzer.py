#!/usr/bin/env python3
"""
代码分析 Agent 示例

使用 Claude Agent SDK 构建一个自动代码分析工具。
该 Agent 可以：
1. 扫描项目目录
2. 识别代码结构
3. 发现潜在问题
4. 生成分析报告

用法:
    python code_analyzer.py <directory>

依赖:
    pip install claude-agent-sdk

环境变量:
    ANTHROPIC_API_KEY - Anthropic API Key
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

try:
    from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
except ImportError:
    print("Error: claude-agent-sdk not installed")
    print("Install with: pip install claude-agent-sdk")
    sys.exit(1)


async def analyze_codebase(directory: str) -> dict:
    """
    使用 Claude Agent SDK 分析代码库

    Args:
        directory: 要分析的目录路径

    Returns:
        包含分析结果的字典
    """
    # 配置 Agent 选项
    options = ClaudeAgentOptions(
        # 只允许读取操作，确保安全
        allowed_tools=["Read", "Grep", "Glob"],

        # 使用只读模式
        permission_mode="plan",

        # 限制执行轮次
        max_turns=25,

        # 设置工作目录
        cwd=directory,

        # 使用 Sonnet 模型（平衡性能和成本）
        model="sonnet"
    )

    # 构建分析提示
    prompt = f"""请分析 {directory} 目录中的代码库。

## 分析任务

1. **项目结构**
   - 识别主要目录和文件
   - 确定项目类型（Web 应用、API、CLI 工具等）
   - 列出使用的技术栈

2. **代码质量**
   - 检查代码组织是否合理
   - 识别重复代码
   - 评估命名规范

3. **潜在问题**
   - 查找可能的 bug
   - 识别安全隐患
   - 发现性能问题

4. **改进建议**
   - 提出具体的改进方案
   - 优先级排序

## 输出格式

请以 Markdown 格式输出报告，包含上述所有部分。
在每个问题后注明文件和行号。
"""

    # 收集结果
    result = {
        "directory": directory,
        "timestamp": datetime.now().isoformat(),
        "report": [],
        "metadata": {}
    }

    try:
        async with ClaudeSDKClient(options=options) as client:
            # 发送查询
            await client.query(prompt)

            # 处理响应
            async for message in client.receive_response():
                match message.type:
                    case "text":
                        # 收集文本输出
                        result["report"].append(message.text)

                    case "tool_use":
                        # 记录使用的工具
                        print(f"  📂 Reading: {message.tool_input.get('file_path', message.tool_input.get('pattern', ''))}")

                    case "result":
                        # 记录元数据
                        result["metadata"] = {
                            "duration_ms": message.duration_ms,
                            "total_cost_usd": message.total_cost_usd,
                            "num_turns": message.num_turns,
                            "input_tokens": message.usage.get("input_tokens", 0),
                            "output_tokens": message.usage.get("output_tokens", 0)
                        }

                    case "error":
                        print(f"  ❌ Error: {message.error}")
                        result["error"] = message.error

    except Exception as e:
        result["error"] = str(e)
        print(f"Error during analysis: {e}")

    return result


def format_report(result: dict) -> str:
    """格式化分析报告"""
    lines = [
        "=" * 60,
        "           CODE ANALYSIS REPORT",
        "=" * 60,
        "",
        f"Directory: {result['directory']}",
        f"Timestamp: {result['timestamp']}",
        ""
    ]

    if result.get("error"):
        lines.extend([
            "⚠️ Analysis encountered an error:",
            result["error"],
            ""
        ])

    lines.extend([
        "-" * 60,
        "                   REPORT",
        "-" * 60,
        ""
    ])

    # 添加报告内容
    report_text = "\n".join(result.get("report", []))
    lines.append(report_text)

    # 添加元数据
    if result.get("metadata"):
        meta = result["metadata"]
        lines.extend([
            "",
            "-" * 60,
            "                 STATISTICS",
            "-" * 60,
            f"Duration: {meta.get('duration_ms', 0) / 1000:.2f}s",
            f"Cost: ${meta.get('total_cost_usd', 0):.4f}",
            f"Turns: {meta.get('num_turns', 0)}",
            f"Tokens: {meta.get('input_tokens', 0)} in / {meta.get('output_tokens', 0)} out",
            "=" * 60
        ])

    return "\n".join(lines)


async def main():
    """主函数"""
    # 检查参数
    if len(sys.argv) < 2:
        print("Usage: python code_analyzer.py <directory>")
        print("Example: python code_analyzer.py ./src")
        sys.exit(1)

    directory = sys.argv[1]

    # 验证目录
    if not Path(directory).is_dir():
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    print(f"🔍 Analyzing codebase: {directory}")
    print("   This may take a few minutes...")
    print()

    # 运行分析
    result = await analyze_codebase(directory)

    # 输出报告
    report = format_report(result)
    print(report)

    # 保存报告到文件
    report_file = f"analysis-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    with open(report_file, "w") as f:
        f.write(report)

    print(f"\n📄 Report saved to: {report_file}")


if __name__ == "__main__":
    asyncio.run(main())
