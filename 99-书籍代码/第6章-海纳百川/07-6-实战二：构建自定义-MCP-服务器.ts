import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// 内存存储
const todos: { id: string; text: string; done: boolean }[] = [];

// 创建 MCP 服务器
const server = new McpServer({
  name: "todo-server",
  version: "1.0.0",
});

// 定义工具：添加待办
server.tool(
  "todo_add",                                     // 工具名称
  "Add a new todo item",                          // 工具描述（Claude 用这个判断何时调用）
  { text: z.string().describe("The todo text") }, // 输入参数 schema
  async ({ text }) => {                           // 执行函数
    const todo = {
      id: Math.random().toString(36).substring(2, 9),
      text,
      done: false,
    };
    todos.push(todo);
    return {
      content: [{ type: "text", text: `Added: ${todo.id} - ${todo.text}` }],
    };
  }
);

// 定义工具：列出待办
server.tool("todo_list", "List all todo items", {}, async () => {
  const text = todos.length === 0
    ? "No todos found."
    : todos.map((t) => `[${t.done ? "x" : " "}] ${t.id}: ${t.text}`).join("\n");
  return { content: [{ type: "text", text }] };
});

// 定义资源：统计信息
server.resource("stats", "Server statistics", async () => {
  return {
    contents: [{
      uri: "stats://current",
      mimeType: "application/json",
      text: JSON.stringify({
        total: todos.length,
        completed: todos.filter((t) => t.done).length,
        pending: todos.filter((t) => !t.done).length,
      }, null, 2),
    }],
  };
});

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP Server started");  // 注意：日志输出到 stderr
}
main().catch(console.error);
