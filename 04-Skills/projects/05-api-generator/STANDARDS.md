# Documentation Standards

## General Principles

1. **Clarity**: Documentation should be clear and unambiguous
2. **Completeness**: Include all necessary information
3. **Consistency**: Follow the same format throughout
4. **Currency**: Keep documentation up to date

## Endpoint Documentation

Each endpoint should document:

### Required Fields
- **Method**: HTTP method (GET, POST, PUT, DELETE, PATCH)
- **Path**: Full endpoint path including base URL
- **Description**: What the endpoint does
- **Parameters**: All input parameters
- **Response**: Expected response format

### Optional Fields
- **Authentication**: Required auth method
- **Rate Limiting**: Any rate limits
- **Deprecation**: If endpoint is deprecated
- **Examples**: Request/response examples

## Parameter Documentation

For each parameter, include:

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Parameter name |
| location | Yes | path, query, header, body |
| type | Yes | Data type |
| required | Yes | true/false |
| description | Yes | What it's for |
| default | No | Default value if optional |
| constraints | No | Validation rules |

## Response Documentation

### Success Response
```markdown
**Status Code**: 200 OK

**Response Body**:
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier |
| ... | ... | ... |
```

### Error Responses
Document common error cases:
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 500 Internal Server Error

## Writing Style

- Use present tense: "Returns a list" not "Will return a list"
- Be direct: "Gets user by ID" not "This endpoint is used to get a user by their ID"
- Use consistent terminology
- Avoid jargon unless well-defined
