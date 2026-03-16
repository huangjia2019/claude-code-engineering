/**
 * 自定义 MCP 服务器示例
 *
 * 这个服务器提供以下功能：
 * 1. todo - 管理待办事项
 * 2. notes - 管理笔记
 * 3. timer - 计时器工具
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// 内存存储
const todos: { id: string; text: string; done: boolean; createdAt: Date }[] = [];
const notes: { id: string; title: string; content: string; createdAt: Date }[] = [];

// 生成唯一 ID
function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}

// 创建 MCP 服务器
const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

// ============ Todo 工具 ============

// 添加待办事项
server.tool(
  "todo_add",
  "Add a new todo item",
  {
    text: z.string().describe("The todo text"),
  },
  async ({ text }) => {
    const todo = {
      id: generateId(),
      text,
      done: false,
      createdAt: new Date(),
    };
    todos.push(todo);

    return {
      content: [
        {
          type: "text",
          text: `Added todo: ${todo.id} - ${todo.text}`,
        },
      ],
    };
  }
);

// 列出待办事项
server.tool(
  "todo_list",
  "List all todo items",
  {
    showDone: z.boolean().optional().describe("Include completed items"),
  },
  async ({ showDone = true }) => {
    const filtered = showDone ? todos : todos.filter((t) => !t.done);

    const text = filtered.length === 0
      ? "No todos found."
      : filtered
          .map((t) => `[${t.done ? "x" : " "}] ${t.id}: ${t.text}`)
          .join("\n");

    return {
      content: [
        {
          type: "text",
          text: `Todos:\n${text}`,
        },
      ],
    };
  }
);

// 完成待办事项
server.tool(
  "todo_complete",
  "Mark a todo as completed",
  {
    id: z.string().describe("The todo ID"),
  },
  async ({ id }) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) {
      return {
        content: [{ type: "text", text: `Todo not found: ${id}` }],
        isError: true,
      };
    }

    todo.done = true;
    return {
      content: [{ type: "text", text: `Completed: ${todo.text}` }],
    };
  }
);

// 删除待办事项
server.tool(
  "todo_delete",
  "Delete a todo item",
  {
    id: z.string().describe("The todo ID"),
  },
  async ({ id }) => {
    const index = todos.findIndex((t) => t.id === id);
    if (index === -1) {
      return {
        content: [{ type: "text", text: `Todo not found: ${id}` }],
        isError: true,
      };
    }

    const [deleted] = todos.splice(index, 1);
    return {
      content: [{ type: "text", text: `Deleted: ${deleted.text}` }],
    };
  }
);

// ============ Notes 工具 ============

// 创建笔记
server.tool(
  "note_create",
  "Create a new note",
  {
    title: z.string().describe("Note title"),
    content: z.string().describe("Note content"),
  },
  async ({ title, content }) => {
    const note = {
      id: generateId(),
      title,
      content,
      createdAt: new Date(),
    };
    notes.push(note);

    return {
      content: [
        {
          type: "text",
          text: `Created note: ${note.id} - ${note.title}`,
        },
      ],
    };
  }
);

// 列出笔记
server.tool(
  "note_list",
  "List all notes",
  {},
  async () => {
    const text = notes.length === 0
      ? "No notes found."
      : notes.map((n) => `${n.id}: ${n.title}`).join("\n");

    return {
      content: [{ type: "text", text: `Notes:\n${text}` }],
    };
  }
);

// 读取笔记
server.tool(
  "note_read",
  "Read a note by ID",
  {
    id: z.string().describe("Note ID"),
  },
  async ({ id }) => {
    const note = notes.find((n) => n.id === id);
    if (!note) {
      return {
        content: [{ type: "text", text: `Note not found: ${id}` }],
        isError: true,
      };
    }

    return {
      content: [
        {
          type: "text",
          text: `# ${note.title}\n\n${note.content}\n\n---\nCreated: ${note.createdAt.toISOString()}`,
        },
      ],
    };
  }
);

// ============ Timer 工具 ============

// 计时器
server.tool(
  "timer",
  "Start a timer and wait for specified duration",
  {
    seconds: z.number().min(1).max(60).describe("Duration in seconds (max 60)"),
    message: z.string().optional().describe("Message to show when timer ends"),
  },
  async ({ seconds, message = "Timer completed!" }) => {
    await new Promise((resolve) => setTimeout(resolve, seconds * 1000));

    return {
      content: [
        {
          type: "text",
          text: `⏰ ${message} (${seconds}s elapsed)`,
        },
      ],
    };
  }
);

// ============ 资源定义 ============

// 定义可读取的资源
server.resource(
  "stats",
  "Server statistics",
  async () => {
    return {
      contents: [
        {
          uri: "stats://current",
          mimeType: "application/json",
          text: JSON.stringify(
            {
              totalTodos: todos.length,
              completedTodos: todos.filter((t) => t.done).length,
              pendingTodos: todos.filter((t) => !t.done).length,
              totalNotes: notes.length,
              serverUptime: process.uptime(),
            },
            null,
            2
          ),
        },
      ],
    };
  }
);

// ============ 启动服务器 ============

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP Server started");
}

main().catch(console.error);
