# FastAPI + SSE 示例（框架代码）
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from claude_agent_sdk import query, AssistantMessage, ResultMessage

app = FastAPI()


@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    async def event_stream():
        async for message in query(prompt=request.prompt, options=options):
            # 用 isinstance 判断，不是 message.type
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if hasattr(block, "text"):
                        yield f"data: {json.dumps({'type': 'text', 'content': block.text})}\n\n"
            elif isinstance(message, ResultMessage):
                yield f"data: {json.dumps({'type': 'done', 'cost': message.total_cost_usd})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
