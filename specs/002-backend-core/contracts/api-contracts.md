# API Contracts: Todo Management Backend

## Base URL
`/api/{user_id}/tasks`

All endpoints are scoped to a specific user identified by `{user_id}` in the path.

## Endpoints

### GET /api/{user_id}/tasks
**Description**: Retrieve all todos for the specified user

**Path Parameters**:
- `user_id`: String - Unique identifier of the user

**Query Parameters**:
- `completed`: Optional boolean - Filter by completion status
- `limit`: Optional integer - Maximum number of results to return
- `offset`: Optional integer - Number of results to skip for pagination

**Response**:
- `200 OK`: Array of Todo objects
- `404 Not Found`: User not found (if applicable)

**Response Body**:
```json
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "created_at": "2023-01-01T10:00:00Z",
    "updated_at": "2023-01-01T10:00:00Z"
  }
]
```

---

### POST /api/{user_id}/tasks
**Description**: Create a new todo for the specified user

**Path Parameters**:
- `user_id`: String - Unique identifier of the user

**Request Body**:
```json
{
  "title": "Task title",
  "description": "Optional task description"
}
```

**Validation**:
- `title` is required and must not be empty
- `title` must be 1-255 characters
- `description` is optional, max 1000 characters

**Response**:
- `201 Created`: Successfully created todo
- `400 Bad Request`: Invalid input data
- `404 Not Found`: User not found (if applicable)

**Response Body**:
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T10:00:00Z"
}
```

---

### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific todo by ID for the specified user

**Path Parameters**:
- `user_id`: String - Unique identifier of the user
- `id`: Integer - ID of the todo item

**Response**:
- `200 OK`: Todo object found
- `404 Not Found`: Todo not found or doesn't belong to user

**Response Body**:
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T10:00:00Z"
}
```

---

### PUT /api/{user_id}/tasks/{id}
**Description**: Update an existing todo for the specified user

**Path Parameters**:
- `user_id`: String - Unique identifier of the user
- `id`: Integer - ID of the todo item

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Validation**:
- At least one field must be provided
- `title` must be 1-255 characters if provided
- `description` max 1000 characters if provided

**Response**:
- `200 OK`: Successfully updated
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Todo not found or doesn't belong to user

**Response Body**:
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T11:00:00Z"
}
```

---

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific todo by ID for the specified user

**Path Parameters**:
- `user_id`: String - Unique identifier of the user
- `id`: Integer - ID of the todo item

**Response**:
- `204 No Content`: Successfully deleted
- `404 Not Found`: Todo not found or doesn't belong to user

---

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Mark a todo as complete/incomplete for the specified user

**Path Parameters**:
- `user_id`: String - Unique identifier of the user
- `id`: Integer - ID of the todo item

**Request Body**:
```json
{
  "completed": true
}
```

**Response**:
- `200 OK`: Successfully updated completion status
- `400 Bad Request`: Invalid completed value
- `404 Not Found`: Todo not found or doesn't belong to user

**Response Body**:
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2023-01-01T10:00:00Z",
  "updated_at": "2023-01-01T11:00:00Z"
}
```

## Common Error Responses

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Detailed error message",
  "details": {
    "field": "validation error details"
  }
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Authentication
All endpoints assume user authentication has been handled by a middleware that validates the user and passes the user_id to the handlers.

## Headers
- `Content-Type: application/json` for requests with bodies
- `Accept: application/json` for responses