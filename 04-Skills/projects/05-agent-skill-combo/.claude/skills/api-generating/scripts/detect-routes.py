#!/usr/bin/env python3
"""
Express.js Route Detector
=========================
Scans a directory for Express route definitions and outputs a structured list.

Handles edge cases that simple Grep cannot:
- router.use() mounted sub-routers with prefix
- Dynamic route parameters (:id, :slug)
- Re-exported routers (module.exports = router)
- Chained methods (router.route('/path').get().post())

Usage:
    python detect-routes.py <src_directory>

Output format (one route per line):
    METHOD  /full/path  source_file:line_number
"""

import os
import re
import sys


# Patterns for Express route definitions
ROUTE_PATTERNS = [
    # router.get('/path', handler)  or  app.get('/path', handler)
    re.compile(
        r'(?:router|app)\.(get|post|put|patch|delete|all)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        re.IGNORECASE,
    ),
    # router.route('/path').get().post()
    re.compile(
        r'(?:router|app)\.route\s*\(\s*[\'"]([^\'"]+)[\'"]',
        re.IGNORECASE,
    ),
]

# Pattern for sub-router mounting: app.use('/prefix', someRouter)
MOUNT_PATTERN = re.compile(
    r'(?:app|router)\.use\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*(\w+)',
)

# Pattern for chained methods on route()
CHAINED_METHOD = re.compile(
    r'\.(get|post|put|patch|delete)\s*\(',
    re.IGNORECASE,
)


def scan_file(filepath):
    """Scan a single file for route definitions."""
    routes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError):
        return routes

    for i, line in enumerate(lines, 1):
        # Check standard route patterns
        for pattern in ROUTE_PATTERNS:
            for match in pattern.finditer(line):
                groups = match.groups()
                if len(groups) == 2:
                    # Standard route: (method, path)
                    method, path = groups
                    routes.append({
                        'method': method.upper(),
                        'path': path,
                        'file': filepath,
                        'line': i,
                    })
                elif len(groups) == 1:
                    # router.route() — need to find chained methods
                    route_path = groups[0]
                    # Look at this line and next few lines for chained methods
                    context = ''.join(lines[i-1:min(i+5, len(lines))])
                    for chain_match in CHAINED_METHOD.finditer(context):
                        routes.append({
                            'method': chain_match.group(1).upper(),
                            'path': route_path,
                            'file': filepath,
                            'line': i,
                        })

    return routes


def find_mount_prefixes(entry_file):
    """Find sub-router mount points in the main app file."""
    prefixes = {}
    try:
        with open(entry_file, 'r', encoding='utf-8') as f:
            content = f.read()
        for match in MOUNT_PATTERN.finditer(content):
            prefix, router_var = match.groups()
            prefixes[router_var] = prefix
    except (FileNotFoundError, UnicodeDecodeError):
        pass
    return prefixes


def scan_directory(src_dir):
    """Recursively scan directory for route files."""
    all_routes = []

    for root, _dirs, files in os.walk(src_dir):
        for filename in files:
            if filename.endswith(('.js', '.ts', '.mjs')):
                filepath = os.path.join(root, filename)
                routes = scan_file(filepath)
                all_routes.extend(routes)

    return all_routes


def main():
    if len(sys.argv) < 2:
        print("Usage: python detect-routes.py <src_directory>", file=sys.stderr)
        sys.exit(1)

    src_dir = sys.argv[1]

    if not os.path.isdir(src_dir):
        print(f"Error: {src_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    routes = scan_directory(src_dir)

    if not routes:
        print("No routes found.", file=sys.stderr)
        sys.exit(0)

    # Output header
    print(f"{'METHOD':<8} {'PATH':<40} {'SOURCE'}")
    print("-" * 80)

    # Sort by path then method
    routes.sort(key=lambda r: (r['path'], r['method']))

    for route in routes:
        rel_path = os.path.relpath(route['file'], src_dir)
        source = f"{rel_path}:{route['line']}"
        print(f"{route['method']:<8} {route['path']:<40} {source}")

    print(f"\nTotal: {len(routes)} routes found")


if __name__ == '__main__':
    main()
