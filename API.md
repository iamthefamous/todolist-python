# API Documentation

## Base URL
```
http://localhost:8080
```

## Endpoints

### Health Check

#### GET `/health`
Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Authentication

### POST `/api/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Fields:**
- `email` (required, string): Valid email address (must be unique)
- `username` (required, string, 3-50 chars): Username (must be unique)
- `password` (required, string, 6-100 chars): User password

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "johndoe",
  "createdAt": "2025-12-25T10:00:00",
  "updatedAt": "2025-12-25T10:00:00"
}
```

**Error Responses:**
- `400 Bad Request`: Email already registered or username already taken
- `422 Unprocessable Entity`: Invalid data format

**Example:**
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

---

### POST `/api/auth/login`
Login with email and password to receive a JWT access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Fields:**
- `email` (required, string): User email address
- `password` (required, string): User password

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid email or password

**Example:**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

---

### GET `/api/auth/me`
Get the current authenticated user's profile.

**Authentication Required:** Yes (JWT Bearer token)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "johndoe",
  "createdAt": "2025-12-25T10:00:00",
  "updatedAt": "2025-12-25T10:00:00"
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token

**Example:**
```bash
# First login to get token
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}' \
  | jq -r '.access_token')

# Then use token to get profile
curl -X GET http://localhost:8080/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## Todo Operations

#### GET `/api/todos`
Get all todos with optional filtering.

**Query Parameters:**
- `completed` (optional, boolean): Filter by completion status
  - `true`: Get only completed todos
  - `false`: Get only active todos
  - omit: Get all todos

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "completed": false,
    "createdAt": "2025-11-24T10:00:00",
    "updatedAt": "2025-11-24T10:00:00"
  }
]
```

**Examples:**
```bash
# Get all todos
curl http://localhost:8080/api/todos

# Get completed todos only
curl http://localhost:8080/api/todos?completed=true

# Get active todos only
curl http://localhost:8080/api/todos?completed=false
```

---

#### GET `/api/todos/{id}`
Get a specific todo by ID.

**Path Parameters:**
- `id` (required, string): MongoDB ObjectId of the todo

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Learn FastAPI",
  "description": "Complete the FastAPI tutorial",
  "completed": false,
  "createdAt": "2025-11-24T10:00:00",
  "updatedAt": "2025-11-24T10:00:00"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid ID format
- `404 Not Found`: Todo with specified ID not found

**Example:**
```bash
curl http://localhost:8080/api/todos/507f1f77bcf86cd799439011
```

---

#### GET `/api/todos/search`
Search todos by title (case-insensitive).

**Query Parameters:**
- `title` (required, string): Search query

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "completed": false,
    "createdAt": "2025-11-24T10:00:00",
    "updatedAt": "2025-11-24T10:00:00"
  }
]
```

**Example:**
```bash
curl "http://localhost:8080/api/todos/search?title=fastapi"
```

---

#### POST `/api/todos`
Create a new todo.

**Request Body:**
```json
{
  "title": "Learn FastAPI",
  "description": "Complete the FastAPI tutorial",
  "completed": false
}
```

**Fields:**
- `title` (required, string, 1-200 chars): Todo title
- `description` (optional, string, max 1000 chars): Todo description
- `completed` (optional, boolean, default: false): Completion status

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Learn FastAPI",
  "description": "Complete the FastAPI tutorial",
  "completed": false,
  "createdAt": "2025-11-24T10:00:00",
  "updatedAt": "2025-11-24T10:00:00"
}
```

**Example:**
```bash
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "completed": false
  }'
```

---

#### PUT `/api/todos/{id}`
Update an existing todo.

**Path Parameters:**
- `id` (required, string): MongoDB ObjectId of the todo

**Request Body:**
All fields are optional. Only include fields you want to update.

```json
{
  "title": "Learn FastAPI - Updated",
  "description": "Complete the advanced FastAPI tutorial",
  "completed": true
}
```

**Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "Learn FastAPI - Updated",
  "description": "Complete the advanced FastAPI tutorial",
  "completed": true,
  "createdAt": "2025-11-24T10:00:00",
  "updatedAt": "2025-11-24T10:30:00"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid ID format
- `404 Not Found`: Todo with specified ID not found

**Example:**
```bash
curl -X PUT http://localhost:8080/api/todos/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

---

#### DELETE `/api/todos/{id}`
Delete a specific todo.

**Path Parameters:**
- `id` (required, string): MongoDB ObjectId of the todo

**Response:** `204 No Content`

**Error Responses:**
- `400 Bad Request`: Invalid ID format
- `404 Not Found`: Todo with specified ID not found

**Example:**
```bash
curl -X DELETE http://localhost:8080/api/todos/507f1f77bcf86cd799439011
```

---

#### DELETE `/api/todos`
Delete all todos.

⚠️ **Warning:** This endpoint is intended for development/testing only. In production, it should be protected with proper authentication/authorization.

**Response:** `204 No Content`

**Example:**
```bash
curl -X DELETE http://localhost:8080/api/todos
```

---

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

These interfaces allow you to:
- View all endpoints and their schemas
- Try out the API directly from your browser
- See request/response examples
- Download the OpenAPI specification

---

## Error Responses

### Validation Error (422)
Returned when request data doesn't match the expected schema.

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found (404)
```json
{
  "detail": "Todo with id 507f1f77bcf86cd799439011 not found"
}
```

### Bad Request (400)
```json
{
  "detail": "Invalid todo ID format"
}
```

---

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000`
- `http://127.0.0.1:5173`
- `http://127.0.0.1:3000`

All HTTP methods and headers are allowed for these origins.
