---
name: codebase-visualizer
description: Generate an interactive tree visualization of your codebase. Use when exploring a new repo or understanding project structure.
allowed-tools:
  - Bash(python *)
---

Run the visualization script from your project root:

```bash
python .claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` and opens it in your default browser.
