# API Index Template

Use this template for the API overview page:

```markdown
# {API_NAME} API Reference

{Brief description of the API and its purpose.}

## Base URL

```
{BASE_URL}
```

## Authentication

{Description of authentication method}

## Endpoints Overview

| Method | Path | Description |
|--------|------|-------------|
| {METHOD} | {PATH} | {BRIEF_DESC} |

## Endpoints

### {CATEGORY_1}

- [{METHOD} {PATH}](#{anchor}) - {Brief description}

### {CATEGORY_2}

- [{METHOD} {PATH}](#{anchor}) - {Brief description}

## Common Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

## Rate Limiting

{Rate limiting information if applicable}

## Versioning

{API versioning information if applicable}
```
