# API Documentation Patterns

## Common Frameworks

### Express.js
```javascript
// Route pattern
app.get('/users/:id', handler)
router.post('/auth/login', authController.login)

// Look for:
// - app.get(), app.post(), etc.
// - router.METHOD()
// - @route decorators (if using decorators)
```

### FastAPI (Python)
```python
# Route pattern
@app.get("/users/{user_id}")
@router.post("/auth/login")

# Look for:
# - @app.METHOD decorators
# - @router.METHOD decorators
# - Pydantic models for schemas
```

### Spring Boot (Java)
```java
// Route pattern
@GetMapping("/users/{id}")
@PostMapping("/auth/login")
@RequestMapping(value = "/api", method = RequestMethod.GET)

// Look for:
// - @XXXMapping annotations
// - @RequestMapping
// - @RestController classes
```

### Go (Gin/Echo)
```go
// Route pattern
r.GET("/users/:id", handler)
e.POST("/auth/login", controller.Login)

// Look for:
// - router.METHOD() calls
// - Group definitions
// - Middleware attachments
```

## Parameter Detection

### Path Parameters
- Express: `:paramName`
- FastAPI: `{param_name}`
- Spring: `{paramName}`
- Go: `:paramName` or `*paramName`

### Query Parameters
Look for:
- `req.query` (Express)
- `Query()` (FastAPI)
- `@RequestParam` (Spring)
- `c.Query()` (Gin)

### Body Parameters
Look for:
- `req.body` (Express)
- Pydantic models (FastAPI)
- `@RequestBody` (Spring)
- `c.Bind()` (Gin)

## Response Detection

### Status Codes
- Look for explicit status codes: `res.status(201)`, `status_code=201`
- Default is usually 200
- Error handlers indicate error codes

### Response Schema
- TypeScript interfaces/types
- Pydantic models
- Java DTOs
- Go structs with json tags
