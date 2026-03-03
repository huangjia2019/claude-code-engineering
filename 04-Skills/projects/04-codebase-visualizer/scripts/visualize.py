#!/usr/bin/env python3
"""
Codebase Visualizer - 生成交互式代码库目录树 HTML

用法:
    python visualize.py [目标目录] [--max-depth N] [--exclude pattern1,pattern2]

示例:
    python visualize.py .
    python visualize.py /path/to/project --max-depth 4
    python visualize.py . --exclude __pycache__,dist,.git

生成 codebase-map.html 并在浏览器中打开。
"""

import os
import sys
import json
import webbrowser
from pathlib import Path
from collections import defaultdict

# 默认忽略的目录和文件
DEFAULT_EXCLUDES = {
    ".git", ".svn", ".hg",
    "node_modules", "__pycache__", ".pytest_cache",
    ".venv", "venv", "env",
    "dist", "build", ".next", ".nuxt",
    ".DS_Store", "Thumbs.db",
    ".claude",
}

# 文件类型 → 颜色映射
FILE_COLORS = {
    ".py": "#3572A5",
    ".js": "#F7DF1E",
    ".ts": "#3178C6",
    ".tsx": "#3178C6",
    ".jsx": "#F7DF1E",
    ".html": "#E34F26",
    ".css": "#1572B6",
    ".json": "#292929",
    ".md": "#083FA1",
    ".yaml": "#CB171E",
    ".yml": "#CB171E",
    ".sh": "#89E051",
    ".go": "#00ADD8",
    ".rs": "#DEA584",
    ".java": "#B07219",
    ".rb": "#CC342D",
    ".php": "#4F5D95",
    ".sql": "#E38C00",
    ".toml": "#9C4121",
}


def scan_directory(root_path, max_depth=6, excludes=None):
    """扫描目录，构建树形结构数据。"""
    if excludes is None:
        excludes = DEFAULT_EXCLUDES

    root = Path(root_path).resolve()
    tree = {"name": root.name, "type": "directory", "children": [], "path": "."}
    stats = defaultdict(int)

    def _scan(current_path, node, depth):
        if depth > max_depth:
            return
        try:
            entries = sorted(current_path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
        except PermissionError:
            return

        for entry in entries:
            if entry.name in excludes:
                continue

            rel_path = str(entry.relative_to(root))

            if entry.is_dir():
                child = {"name": entry.name, "type": "directory", "children": [], "path": rel_path}
                _scan(entry, child, depth + 1)
                if child["children"]:  # 只保留非空目录
                    node["children"].append(child)
            elif entry.is_file():
                ext = entry.suffix.lower()
                size = entry.stat().st_size
                stats[ext] += 1
                child = {
                    "name": entry.name,
                    "type": "file",
                    "ext": ext,
                    "size": size,
                    "path": rel_path,
                }
                node["children"].append(child)

    _scan(root, tree, 0)
    return tree, dict(stats)


def generate_html(tree_data, stats, project_name):
    """生成交互式 HTML 可视化页面。"""

    stats_json = json.dumps(dict(sorted(stats.items(), key=lambda x: -x[1])[:15]), ensure_ascii=False)
    tree_json = json.dumps(tree_data, ensure_ascii=False, indent=None)
    colors_json = json.dumps(FILE_COLORS, ensure_ascii=False)

    total_files = sum(stats.values())
    total_types = len(stats)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project_name} - Codebase Map</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }}
h1 {{ color: #58a6ff; font-size: 1.4em; margin-bottom: 8px; }}
.stats {{ color: #8b949e; font-size: 0.85em; margin-bottom: 16px; }}
.stats span {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 2px 10px; margin-right: 6px; display: inline-block; margin-bottom: 4px; }}
.tree {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; overflow-x: auto; }}
.tree ul {{ list-style: none; padding-left: 20px; }}
.tree > ul {{ padding-left: 0; }}
.tree li {{ line-height: 1.8; white-space: nowrap; }}
.tree li.dir > .label {{ cursor: pointer; user-select: none; }}
.tree li.dir > .label:hover {{ color: #58a6ff; }}
.tree li.dir > .label::before {{ content: '\\25BE '; color: #8b949e; display: inline-block; width: 16px; transition: transform 0.15s; }}
.tree li.dir.collapsed > .label::before {{ content: '\\25B8 '; }}
.tree li.dir.collapsed > ul {{ display: none; }}
.tree li.file .label {{ color: #c9d1d9; }}
.tree li.file .label::before {{ content: '  '; display: inline-block; width: 16px; }}
.icon {{ display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; vertical-align: middle; }}
.path {{ color: #484f58; font-size: 0.75em; margin-left: 8px; }}
.size {{ color: #484f58; font-size: 0.75em; margin-left: 6px; }}
.bar-chart {{ margin-top: 16px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; }}
.bar-chart h3 {{ color: #58a6ff; font-size: 1em; margin-bottom: 12px; }}
.bar {{ display: flex; align-items: center; margin-bottom: 4px; }}
.bar-label {{ width: 60px; text-align: right; font-size: 0.8em; color: #8b949e; padding-right: 8px; }}
.bar-fill {{ height: 16px; border-radius: 3px; min-width: 2px; transition: width 0.3s; }}
.bar-count {{ font-size: 0.8em; color: #8b949e; padding-left: 6px; }}
.controls {{ margin-bottom: 12px; }}
.controls button {{ background: #21262d; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; padding: 4px 12px; cursor: pointer; font-size: 0.8em; margin-right: 4px; }}
.controls button:hover {{ background: #30363d; }}
</style>
</head>
<body>
<h1>{project_name}</h1>
<div class="stats">
    <span>{total_files} files</span>
    <span>{total_types} types</span>
</div>
<div class="controls">
    <button onclick="expandAll()">Expand All</button>
    <button onclick="collapseAll()">Collapse All</button>
    <button onclick="collapseDepth(1)">Depth 1</button>
    <button onclick="collapseDepth(2)">Depth 2</button>
</div>
<div class="tree" id="tree"></div>
<div class="bar-chart" id="chart"></div>

<script>
const TREE = {tree_json};
const STATS = {stats_json};
const COLORS = {colors_json};

function getColor(ext) {{ return COLORS[ext] || '#8b949e'; }}

function formatSize(bytes) {{
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}}

function buildTree(node, depth) {{
    if (node.type === 'file') {{
        const color = getColor(node.ext);
        return '<li class="file"><span class="label">'
            + '<span class="icon" style="background:' + color + '"></span>'
            + node.name
            + '<span class="size">' + formatSize(node.size) + '</span>'
            + '</span></li>';
    }}
    const collapsed = depth > 1 ? ' collapsed' : '';
    let html = '<li class="dir' + collapsed + '">'
        + '<span class="label" onclick="toggleDir(this)">' + node.name + '/</span>';
    if (node.children && node.children.length > 0) {{
        html += '<ul>';
        for (const child of node.children) {{
            html += buildTree(child, depth + 1);
        }}
        html += '</ul>';
    }}
    html += '</li>';
    return html;
}}

function toggleDir(el) {{
    el.parentElement.classList.toggle('collapsed');
}}

function expandAll() {{
    document.querySelectorAll('.tree .dir').forEach(el => el.classList.remove('collapsed'));
}}

function collapseAll() {{
    document.querySelectorAll('.tree .dir').forEach(el => el.classList.add('collapsed'));
}}

function collapseDepth(maxDepth) {{
    function setDepth(el, depth) {{
        if (!el.classList.contains('dir')) return;
        if (depth >= maxDepth) {{
            el.classList.add('collapsed');
        }} else {{
            el.classList.remove('collapsed');
        }}
        el.querySelectorAll(':scope > ul > .dir').forEach(child => setDepth(child, depth + 1));
    }}
    document.querySelectorAll('.tree > ul > .dir').forEach(el => setDepth(el, 0));
}}

function buildChart() {{
    const entries = Object.entries(STATS);
    if (entries.length === 0) return;
    const maxCount = Math.max(...entries.map(e => e[1]));
    let html = '<h3>File Types</h3>';
    for (const [ext, count] of entries) {{
        const pct = (count / maxCount * 100).toFixed(0);
        const color = getColor(ext);
        html += '<div class="bar">'
            + '<span class="bar-label">' + (ext || '(none)') + '</span>'
            + '<span class="bar-fill" style="width:' + pct + '%;background:' + color + '"></span>'
            + '<span class="bar-count">' + count + '</span>'
            + '</div>';
    }}
    document.getElementById('chart').innerHTML = html;
}}

document.getElementById('tree').innerHTML = '<ul>' + buildTree(TREE, 0) + '</ul>';
buildChart();
</script>
</body>
</html>"""
    return html


def main():
    target = "."
    max_depth = 6
    excludes = set(DEFAULT_EXCLUDES)

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--max-depth" and i + 1 < len(args):
            max_depth = int(args[i + 1])
            i += 2
        elif args[i] == "--exclude" and i + 1 < len(args):
            for pat in args[i + 1].split(","):
                excludes.add(pat.strip())
            i += 2
        elif not args[i].startswith("-"):
            target = args[i]
            i += 1
        else:
            i += 1

    target_path = Path(target).resolve()
    if not target_path.is_dir():
        print(f"Error: '{target}' is not a directory")
        sys.exit(1)

    project_name = target_path.name
    print(f"Scanning {project_name}...")

    tree_data, stats = scan_directory(target_path, max_depth, excludes)

    total = sum(stats.values())
    print(f"Found {total} files across {len(stats)} types")

    output_file = "codebase-map.html"
    html = generate_html(tree_data, stats, project_name)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    abs_path = Path(output_file).resolve()
    print(f"Generated: {abs_path}")

    try:
        webbrowser.open(f"file://{abs_path}")
        print("Opened in browser.")
    except Exception:
        print("Could not open browser automatically. Open the file manually.")


if __name__ == "__main__":
    main()
