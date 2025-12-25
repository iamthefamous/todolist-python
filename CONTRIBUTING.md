# Contributing to TodoList Application

Thank you for your interest in contributing to the TodoList application!

## Development Setup

### Prerequisites

- Python 3.11 or higher
- MongoDB 7.0+ or Docker
- Git

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iamthefamous/todolist-python.git
   cd todolist-python
   ```

2. **Start MongoDB:**
   ```bash
   docker compose up -d mongodb
   ```

3. **Set up the backend:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

5. **Run the server:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

   Or use the startup script:
   ```bash
   ./start-backend.sh
   ```

## Code Style

### Python Code Style

This project follows PEP 8 style guidelines with some exceptions:

- **Line Length**: 100 characters (relaxed from 79)
- **Imports**: Group imports in this order:
  1. Standard library
  2. Third-party packages
  3. Local application imports

### Type Hints

Always use type hints for function parameters and return values:

```python
async def get_todos(completed: Optional[bool] = None) -> List[TodoResponse]:
    ...
```

### Documentation

- Use docstrings for all public functions and classes
- Follow Google-style docstrings format
- Include parameter descriptions and return types

```python
async def create_todo(todo: TodoCreate):
    """
    Create a new todo
    - **title**: Title of the todo (required)
    - **description**: Description of the todo (optional)
    - **completed**: Completion status (default: false)
    """
```

## Project Structure

```
backend/
├── app/
│   ├── config/         # Configuration files
│   │   └── database.py # Database connection
│   ├── models/         # Pydantic models
│   │   └── todo.py     # Todo models
│   ├── routers/        # API route handlers
│   │   └── todo.py     # Todo endpoints
│   └── main.py         # FastAPI application
├── tests/              # Test files
├── requirements.txt    # Dependencies
└── Dockerfile          # Container configuration
```

## Adding New Features

### Adding a New Endpoint

1. **Define the model** in `app/models/`:
   ```python
   class NewModel(BaseModel):
       field: str
   ```

2. **Create the router** in `app/routers/`:
   ```python
   @router.get("/new-endpoint")
   async def new_endpoint():
       ...
   ```

3. **Register the router** in `app/main.py`:
   ```python
   app.include_router(new_router)
   ```

4. **Add tests** in `tests/`:
   ```python
   def test_new_endpoint():
       ...
   ```

## Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Writing Tests

Use `pytest` with `httpx.AsyncClient` for testing endpoints:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/todos", json={
            "title": "Test Todo",
            "completed": False
        })
        assert response.status_code == 201
```

## Database Schema

The application uses MongoDB with the following schema:

### Todo Document
```javascript
{
  _id: ObjectId,           // Auto-generated
  title: String,           // Required, 1-200 chars
  description: String,     // Optional, max 1000 chars
  completed: Boolean,      // Default: false
  createdAt: ISODate,      // Auto-generated
  updatedAt: ISODate       // Auto-updated
}
```

## API Design Guidelines

### RESTful Principles

- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Return appropriate status codes
- Use plural nouns for collections (`/todos` not `/todo`)
- Use IDs in paths for specific resources (`/todos/{id}`)

### Status Codes

- `200 OK`: Successful GET, PUT
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

### Response Format

Always return JSON with consistent structure:

```json
{
  "id": "...",
  "field1": "...",
  "field2": "..."
}
```

For errors:
```json
{
  "detail": "Error message"
}
```

## Pull Request Process

1. **Fork the repository** and create a new branch
2. **Make your changes** following the code style guidelines
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

### PR Checklist

- [ ] Code follows the project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Commit messages are clear and descriptive

## Security

### Reporting Vulnerabilities

If you discover a security vulnerability, please email the maintainer directly. Do not create a public issue.

### Security Best Practices

- Never commit credentials or secrets
- Use environment variables for configuration
- Validate all user inputs
- Use parameterized queries (MongoDB automatically does this)
- Keep dependencies up to date

## Questions?

If you have questions or need help:

1. Check the README.md
2. Check the API.md documentation
3. Open an issue on GitHub

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Code of Conduct

Be respectful and professional in all interactions. We want to maintain a welcoming and inclusive environment for all contributors.
