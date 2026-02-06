# API Contracts: Todo Application Frontend

## Authentication Endpoints (Consumed by Frontend)

### POST /api/auth/signup
**Request**: { email: string, password: string }
**Response**: { user: User, token: JWT }
**Headers**: Content-Type: application/json
**Error Responses**: 400 (validation), 409 (email exists)

### POST /api/auth/signin
**Request**: { email: string, password: string }
**Response**: { user: User, token: JWT }
**Headers**: Content-Type: application/json
**Error Responses**: 400 (validation), 401 (invalid credentials)

### POST /api/auth/logout
**Request**: {}
**Response**: { success: boolean }
**Headers**: Authorization: Bearer {token}
**Error Responses**: 401 (invalid token)

## Todo Management Endpoints (Consumed by Frontend)

### GET /api/todos
**Request**: {}
**Response**: { data: Todo[] }
**Headers**: Authorization: Bearer {token}
**Error Responses**: 401 (invalid token)

### POST /api/todos
**Request**: { title: string, description?: string }
**Response**: { data: Todo }
**Headers**: Authorization: Bearer {token}, Content-Type: application/json
**Error Responses**: 400 (validation), 401 (invalid token)

### PUT /api/todos/{id}
**Request**: { title?: string, description?: string, completed?: boolean }
**Response**: { data: Todo }
**Headers**: Authorization: Bearer {token}, Content-Type: application/json
**Error Responses**: 400 (validation), 401 (invalid token), 404 (todo not found)

### DELETE /api/todos/{id}
**Request**: {}
**Response**: { success: boolean }
**Headers**: Authorization: Bearer {token}
**Error Responses**: 401 (invalid token), 404 (todo not found)

### PATCH /api/todos/{id}/toggle
**Request**: { completed: boolean }
**Response**: { data: Todo }
**Headers**: Authorization: Bearer {token}, Content-Type: application/json
**Error Responses**: 401 (invalid token), 404 (todo not found)