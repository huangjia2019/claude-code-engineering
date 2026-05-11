// TypeScript Agent SDK 示例
import { query } from "@anthropic-ai/claude-agent-sdk";

async function reviewPR(changedFiles: string[]) {
  let sessionId: string | undefined;
  let result: string = "";

  for await (const message of query({
    prompt: `审查以下文件的代码变更：${changedFiles.join(", ")}`,
    options: {
      allowedTools: ["Read", "Grep", "Glob"],
      maxTurns: 10,
      maxBudgetUsd: 0.50,
      model: "claude-sonnet-4-6",
      outputFormat: { type: "json_schema", schema: reviewSchema },
    },
  })) {
    if (message.type === "system" && message.subtype === "init") {
      sessionId = message.session_id;
    }
    if (message.type === "result" && message.structured_output) {
      result = message.structured_output;
    }
  }

  return { sessionId, result };
}
