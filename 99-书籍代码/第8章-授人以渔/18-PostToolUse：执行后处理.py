async def auto_format_on_write(input_data, tool_use_id, context):
    """写入文件后自动格式化"""
    if input_data["tool_name"] not in ["Write", "Edit"]:
        return {}

    file_path = input_data["tool_input"].get("file_path", "")
    import subprocess

    if file_path.endswith(".py"):
        subprocess.run(["black", file_path], capture_output=True)
    elif file_path.endswith((".ts", ".js", ".tsx", ".jsx")):
        subprocess.run(["prettier", "--write", file_path], capture_output=True)

    return {}

async def audit_all_tools(input_data, tool_use_id, context):
    """审计所有工具调用"""
    import json
    from datetime import datetime

    entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": input_data["tool_name"],
        "input": input_data["tool_input"],
        "tool_use_id": tool_use_id,
    }
    with open("agent-audit.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return {}

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [...],  # 上面定义的安全 hooks
        "PostToolUse": [
            HookMatcher(matcher="Write", hooks=[auto_format_on_write]),
            HookMatcher(matcher="Edit", hooks=[auto_format_on_write]),
            HookMatcher(matcher="*", hooks=[audit_all_tools]),
        ]
    }
)
