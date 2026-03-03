# Endpoint Documentation Template

Use this template for each API endpoint:

```markdown
## {METHOD} {PATH}

{Brief description of what this endpoint does.}

### Authentication
{Required | Optional | None}

### Parameters

| Name | Location | Type | Required | Description |
|------|----------|------|----------|-------------|
| {name} | {path/query/header/body} | {type} | {Yes/No} | {description} |

### Request Body
{If applicable}

```json
{
  "field": "value"
}
```

### Responses

#### {Status Code} {Status Text}
{Description of when this response occurs}

```json
{
  "example": "response"
}
```

### Example

**Request**:
```bash
curl -X {METHOD} '{BASE_URL}{PATH}' \
  -H 'Content-Type: application/json' \
  -d '{request_body}'
```

**Response**:
```json
{
  "example": "response"
}
```

### Notes
{Any additional information, caveats, or related endpoints}
```
