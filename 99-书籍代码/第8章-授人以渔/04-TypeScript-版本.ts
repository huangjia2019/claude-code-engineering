import { query, ClaudeAgentOptions } from '@anthropic-ai/claude-agent-sdk';

const options: ClaudeAgentOptions = {
    maxTurns: 5,
    allowedTools: ['Read', 'Grep', 'Glob'],
    systemPrompt: '你是一名代码架构分析师。',
};

async function analyzeCode() {
    for await (const message of query({
        prompt: '分析 src/auth/ 目录的实现架构',
        options,
    })) {
        if (message.type === 'assistant') {
            for (const block of message.content) {
                if ('text' in block) {
                    process.stdout.write(block.text);
                }
            }
        } else if (message.type === 'result') {
            console.log(`\n\n完成。费用：$${message.totalCostUsd}`);
        }
    }
}

analyzeCode();
