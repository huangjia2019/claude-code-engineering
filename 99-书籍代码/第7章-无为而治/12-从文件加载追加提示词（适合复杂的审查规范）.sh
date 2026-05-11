claude -p "提取代码中所有安全问题" \
  --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "issues": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
            "file": {"type": "string"},
            "line": {"type": "number"},
            "description": {"type": "string"}
          },
          "required": ["severity", "file", "description"]
        }
      }
    },
    "required": ["issues"]
  }'
