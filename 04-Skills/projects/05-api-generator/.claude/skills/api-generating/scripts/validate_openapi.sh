#!/bin/bash
#
# OpenAPI Specification Validator
#
# Usage:
#   ./validate_openapi.sh <spec_file>
#
# Validates an OpenAPI 3.0 specification file using spectral or openapi-generator-cli
# if available, otherwise performs basic YAML validation.
#

set -e

SPEC_FILE="$1"

if [ -z "$SPEC_FILE" ]; then
    echo "Usage: $0 <spec_file>"
    exit 1
fi

if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: File not found: $SPEC_FILE"
    exit 1
fi

echo "Validating OpenAPI spec: $SPEC_FILE"
echo "================================"

# Try spectral first (most comprehensive)
if command -v spectral &> /dev/null; then
    echo "Using Spectral for validation..."
    spectral lint "$SPEC_FILE"
    exit $?
fi

# Try openapi-generator-cli
if command -v openapi-generator-cli &> /dev/null; then
    echo "Using openapi-generator-cli for validation..."
    openapi-generator-cli validate -i "$SPEC_FILE"
    exit $?
fi

# Try swagger-cli
if command -v swagger-cli &> /dev/null; then
    echo "Using swagger-cli for validation..."
    swagger-cli validate "$SPEC_FILE"
    exit $?
fi

# Fallback to basic YAML validation with Python
if command -v python3 &> /dev/null; then
    echo "Using Python for basic YAML validation..."
    python3 -c "
import yaml
import sys

try:
    with open('$SPEC_FILE', 'r') as f:
        spec = yaml.safe_load(f)

    # Basic structure checks
    required_fields = ['openapi', 'info', 'paths']
    missing = [f for f in required_fields if f not in spec]

    if missing:
        print(f'Error: Missing required fields: {missing}')
        sys.exit(1)

    if not spec['openapi'].startswith('3.'):
        print(f'Warning: OpenAPI version {spec[\"openapi\"]} may not be 3.x')

    print(f'Basic validation passed!')
    print(f'  - OpenAPI version: {spec[\"openapi\"]}')
    print(f'  - API title: {spec[\"info\"].get(\"title\", \"N/A\")}')
    print(f'  - Paths defined: {len(spec[\"paths\"])}')

except yaml.YAMLError as e:
    print(f'YAML parsing error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'Validation error: {e}')
    sys.exit(1)
"
    exit $?
fi

echo "Warning: No validation tool found."
echo "Install one of: spectral, openapi-generator-cli, swagger-cli, or python3 with pyyaml"
exit 1
