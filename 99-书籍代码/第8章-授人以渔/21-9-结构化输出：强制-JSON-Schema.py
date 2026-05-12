from pydantic import BaseModel
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage


class SecurityReport(BaseModel):
    summary: str
    issues: list[dict]     # [{severity, file, line, description}]
    risk_score: float       # 0.0 - 10.0


options = ClaudeAgentOptions(
    output_format={
        "type": "json_schema",
        "schema": SecurityReport.model_json_schema(),
    },
    max_turns=10,
    allowed_tools=["Read", "Grep", "Glob"],
)

async for message in query(prompt="对 src/ 进行安全审查", options=options):
    if isinstance(message, ResultMessage) and message.structured_output:
        report = SecurityReport.model_validate(message.structured_output)
        # report 是类型安全的 Pydantic 对象
        print(f"风险评分：{report.risk_score}")
        for issue in report.issues:
            print(f"  [{issue['severity']}] {issue['file']}:{issue.get('line', '?')} - {issue['description']}")
