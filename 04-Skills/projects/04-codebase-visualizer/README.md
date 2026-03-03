# 项目 06：代码库可视化 Skill

> 第 8 讲配套项目 —— 脚本进阶模式：可视化输出

## 核心理念

这个项目演示渐进式披露的极致形态：**SKILL.md 只有 10 行指令，全部逻辑封装在 Python 脚本中。**

Claude 不需要理解 HTML/CSS/JS 的实现细节（节省 2000+ tokens），只需要知道"运行什么命令"（~10 tokens）。

## 项目结构

```
06-codebase-visualizer/
├── README.md                                    # 本文件
├── SKILL.md                                     # 平铺展示（方便阅读）
├── scripts/
│   └── visualize.py                             # 平铺展示（方便阅读）
└── .claude/skills/codebase-visualizer/          # 标准 Skill 部署结构
    ├── SKILL.md
    └── scripts/
        └── visualize.py
```

## 使用方式

### 直接运行脚本

```bash
cd 04-Skills/projects/06-codebase-visualizer
python scripts/visualize.py ../../..    # 可视化整个课程仓库
```

生成 `codebase-map.html`，用浏览器打开即可看到交互式目录树。

### 通过 Claude Code 使用

将 `.claude/skills/codebase-visualizer/` 复制到你的项目根目录下的 `.claude/skills/`，然后对 Claude 说：

> "帮我可视化一下这个项目的代码结构"

Claude 会自动匹配 `codebase-visualizer` Skill 并执行脚本。

## 教学要点

1. **Token 极致节省**：SKILL.md < 10 行，所有复杂逻辑在脚本中
2. **Skills × Tools 编排**：Skill 告诉 Claude "运行什么"，脚本负责"怎么运行"
3. **可视化输出模式**：脚本生成 HTML → 浏览器打开，适用于各种分析场景
4. **零依赖**：只用 Python 标准库，无需 pip install
