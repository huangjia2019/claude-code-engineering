#!/usr/bin/env python3
"""
API Route Detector

Scans source files and detects API route definitions.

Usage:
    python detect_routes.py <source_directory> [--framework express|fastapi|spring|gin]

Output:
    JSON array of detected routes with method, path, and source location.
"""

import os
import re
import json
import argparse
from pathlib import Path


# Framework-specific patterns
PATTERNS = {
    'express': [
        r'app\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'router\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',
    ],
    'fastapi': [
        r'@app\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        r'@router\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)[\'"]',
    ],
    'spring': [
        r'@(Get|Post|Put|Delete|Patch)Mapping\s*\(\s*[\'"]?([^\'")\s]+)',
        r'@RequestMapping\s*\([^)]*value\s*=\s*[\'"]([^\'"]+)[\'"]',
    ],
    'gin': [
        r'\.(GET|POST|PUT|DELETE|PATCH)\s*\(\s*[\'"]([^\'"]+)[\'"]',
    ]
}

FILE_EXTENSIONS = {
    'express': ['.js', '.ts'],
    'fastapi': ['.py'],
    'spring': ['.java'],
    'gin': ['.go'],
}


def detect_routes(directory, framework=None):
    """Scan directory for API routes."""
    routes = []

    frameworks = [framework] if framework else PATTERNS.keys()

    for fw in frameworks:
        extensions = FILE_EXTENSIONS.get(fw, [])
        patterns = PATTERNS.get(fw, [])

        for root, dirs, files in os.walk(directory):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', 'vendor']]

            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        for pattern in patterns:
                            for match in re.finditer(pattern, content, re.IGNORECASE):
                                method = match.group(1).upper()
                                path = match.group(2)
                                line_num = content[:match.start()].count('\n') + 1

                                routes.append({
                                    'method': method,
                                    'path': path,
                                    'file': filepath,
                                    'line': line_num,
                                    'framework': fw
                                })
                    except Exception as e:
                        print(f"Warning: Could not read {filepath}: {e}")

    return routes


def main():
    parser = argparse.ArgumentParser(description='Detect API routes in source code')
    parser.add_argument('directory', help='Source directory to scan')
    parser.add_argument('--framework', choices=['express', 'fastapi', 'spring', 'gin'],
                        help='Specific framework to detect')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')

    args = parser.parse_args()

    routes = detect_routes(args.directory, args.framework)

    output = json.dumps(routes, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Found {len(routes)} routes, saved to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
