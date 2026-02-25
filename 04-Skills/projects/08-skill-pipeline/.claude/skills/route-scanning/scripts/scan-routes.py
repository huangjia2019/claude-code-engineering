#!/usr/bin/env python3
"""
Express Route Scanner - Pipeline Stage 1
=========================================
Scans Express.js source files for route definitions.
Outputs a structured list for downstream pipeline stages.

Usage:
    python scan-routes.py <source_directory>
"""

import os
import re
import sys
import json


ROUTE_PATTERNS = [
    # router.get('/path', ...) or app.get('/path', ...)
    re.compile(
        r'(?:router|app)\.(get|post|put|patch|delete)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        re.IGNORECASE,
    ),
    # router.route('/path')
    re.compile(
        r'(?:router|app)\.route\s*\(\s*[\'"]([^\'"]+)[\'"]',
        re.IGNORECASE,
    ),
]

CHAINED_METHOD = re.compile(
    r'\.(get|post|put|patch|delete)\s*\(',
    re.IGNORECASE,
)

MIDDLEWARE_PATTERN = re.compile(
    r'(?:requireAuth|isAdmin|validate|authenticate|authorize)\w*',
)


def scan_file(filepath):
    routes = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except (UnicodeDecodeError, PermissionError):
        return routes

    for i, line in enumerate(lines, 1):
        for pattern in ROUTE_PATTERNS:
            for match in pattern.finditer(line):
                groups = match.groups()
                if len(groups) == 2:
                    method, path = groups
                    middleware = MIDDLEWARE_PATTERN.findall(line)
                    routes.append({
                        'method': method.upper(),
                        'path': path,
                        'file': filepath,
                        'line': i,
                        'middleware': middleware,
                        'type': 'standard',
                    })
                elif len(groups) == 1:
                    route_path = groups[0]
                    context = ''.join(lines[i-1:min(i+5, len(lines))])
                    for chain_match in CHAINED_METHOD.finditer(context):
                        middleware = MIDDLEWARE_PATTERN.findall(context)
                        routes.append({
                            'method': chain_match.group(1).upper(),
                            'path': route_path,
                            'file': filepath,
                            'line': i,
                            'middleware': list(set(middleware)),
                            'type': 'chained',
                        })
    return routes


def scan_directory(src_dir):
    all_routes = []
    for root, _dirs, files in os.walk(src_dir):
        for filename in files:
            if filename.endswith(('.js', '.ts', '.mjs')):
                filepath = os.path.join(root, filename)
                all_routes.extend(scan_file(filepath))
    return all_routes


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan-routes.py <src_directory>", file=sys.stderr)
        sys.exit(1)

    src_dir = sys.argv[1]
    if not os.path.isdir(src_dir):
        print(f"Error: {src_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print("=== ROUTE SCANNER (PIPELINE STAGE 1) ===", file=sys.stderr)

    routes = scan_directory(src_dir)

    # Output as JSON for downstream consumption
    print(json.dumps(routes, indent=2))

    print(f"\nTotal: {len(routes)} routes found", file=sys.stderr)


if __name__ == '__main__':
    main()
