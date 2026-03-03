# API Documentation Examples

## Example 1: Simple Express.js Endpoint

### Input Code
```javascript
// routes/users.js
router.get('/users/:id', async (req, res) => {
  const { id } = req.params;
  const user = await User.findById(id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});
```

### Generated Documentation
```markdown
## GET /users/:id

Retrieve a user by their unique identifier.

### Parameters

| Name | Location | Type | Required | Description |
|------|----------|------|----------|-------------|
| id | path | string | Yes | The unique identifier of the user |

### Responses

#### 200 OK
Returns the user object.

```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

#### 404 Not Found
User with specified ID does not exist.

```json
{
  "error": "User not found"
}
```
```

---

## Example 2: FastAPI with Pydantic

### Input Code
```python
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """Create a new user account."""
    # ... implementation
    return new_user
```

### Generated Documentation
```markdown
## POST /users

Create a new user account.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | User's display name |
| email | string | Yes | User's email address |
| password | string | Yes | User's password |

**Example**:
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "securePassword123"
}
```

### Responses

#### 201 Created
User successfully created.

```json
{
  "id": "456",
  "name": "Jane Smith",
  "email": "jane@example.com"
}
```
```

---

## Example 3: OpenAPI Spec Output

### Generated OpenAPI YAML
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
```
