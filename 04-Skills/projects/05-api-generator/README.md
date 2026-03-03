# API Documentation Generator Skill

A production-ready skill for generating API documentation from source code.

## Features

- **Multi-framework support**: Express.js, FastAPI, Spring Boot, Go (Gin/Echo)
- **Multiple output formats**: Markdown, OpenAPI 3.0
- **Automated route detection**: Python script for batch processing
- **Validation tools**: OpenAPI spec validation

## Structure

```
04-api-generator/
├── SKILL.md                    # Main skill file
├── PATTERNS.md                 # Framework detection patterns
├── STANDARDS.md                # Documentation standards
├── EXAMPLES.md                 # Input/output examples
├── templates/
│   ├── index.md               # API index template
│   ├── endpoint.md            # Endpoint documentation template
│   └── openapi.yaml           # OpenAPI spec template
└── scripts/
    ├── detect_routes.py       # Route detection script
    └── validate_openapi.sh    # OpenAPI validation script
```

## Usage Examples

### Single Endpoint Documentation

Ask Claude to document a specific endpoint:
```
Please document this Express route:
router.get('/users/:id', userController.getUser);
```

### Batch Documentation

Scan an entire directory:
```
Scan the src/routes directory and generate API documentation for all endpoints.
```

### OpenAPI Generation

Generate an OpenAPI specification:
```
Generate an OpenAPI 3.0 spec for the API defined in src/api.
```

## Scripts

### Route Detection

```bash
# Detect all routes
python scripts/detect_routes.py src/

# Detect Express routes only
python scripts/detect_routes.py src/ --framework express

# Save to file
python scripts/detect_routes.py src/ -o routes.json
```

### OpenAPI Validation

```bash
# Validate an OpenAPI spec
./scripts/validate_openapi.sh api-spec.yaml
```

## allowed-tools Configuration

This skill uses:
- `Read` - Read source files
- `Grep` - Search for route patterns
- `Glob` - Find files
- `Write` - Create documentation files
- `Bash(python:*)` - Run Python scripts
- `Bash(./scripts/*:*)` - Run project scripts

No `Edit` permission - this skill creates new files but doesn't modify existing ones.
