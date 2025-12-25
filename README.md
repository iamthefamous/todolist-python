# 📝 TodoList Application

A full-stack TodoList application built with **Vite + React** (frontend), **Python FastAPI** (backend), and **MongoDB** (database).

## 🚀 Features

- ✅ Create, Read, Update, and Delete todos (CRUD operations)
- ✅ Mark todos as complete/incomplete
- ✅ Edit todo title and description
- ✅ Filter todos (All, Active, Completed)
- ✅ Search todos by title
- ✅ User authentication with JWT tokens
- ✅ Secure password hashing with bcrypt
- ✅ User registration and login
- ✅ Protected API endpoints
- ✅ Responsive and modern UI
- ✅ RESTful API architecture
- ✅ MongoDB database integration
- ✅ Async/await support with Motor

## 🏗️ Project Structure

```
todolist-python/
├── app/                       # FastAPI backend application
│   ├── config/                # Database configuration
│   ├── models/                # Pydantic models
│   ├── routers/               # API routes
│   └── main.py                # FastAPI application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── .env.example               # Environment variables template
├── docker-compose.yml         # Docker Compose configuration
├── fly.toml                   # Fly.io deployment config
└── start-backend.sh           # Backend startup script
```

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.11** or higher
- **MongoDB 7.0+** (or Docker to run MongoDB in a container)
- **Node.js 18+** and **npm** (for frontend, if applicable)

## 🗄️ Database Setup

### Option 1: Using Docker (Recommended)

The easiest way to run MongoDB is using Docker:

```bash
docker-compose up -d mongodb
```

This will start MongoDB on port 27017.

### Option 2: Manual MongoDB Installation

1. Install and start MongoDB server

2. MongoDB will run on the default port 27017

3. Update database URL in `.env`:
   ```
   MONGODB_URL=mongodb://localhost:27017
   ```

## 🚀 Running the Application

### Quick Start

For the easiest setup experience, use the provided shell script:

1. **Start the database** (if using Docker):
   ```bash
   docker-compose up -d mongodb
   ```

2. **Start the backend**:
   ```bash
   ./start-backend.sh
   ```

3. Open your browser at `http://localhost:8080/docs` for API documentation

### Manual Setup

#### Backend (FastAPI)

1. Create a virtual environment in the project root:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

4. Start the development server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

5. The backend server will start at `http://localhost:8080`
   - API documentation: `http://localhost:8080/docs`
   - Alternative docs: `http://localhost:8080/redoc`

## 🚀 Deployment to Fly.io

This application is ready to be deployed to Fly.io using the provided configuration.

### Prerequisites

1. Install the Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Sign up for a Fly.io account: https://fly.io/app/sign-up

### Deployment Steps

1. **Login to Fly.io:**
   ```bash
   flyctl auth login
   ```

2. **Create a MongoDB database on Fly.io:**
   
   You can either:
   - Use MongoDB Atlas (recommended for production)
   - Deploy MongoDB on Fly.io as a separate app
   
   For MongoDB Atlas:
   ```bash
   # Get your connection string from MongoDB Atlas
   # Example: mongodb+srv://username:password@cluster.mongodb.net/todolist_db
   ```

3. **Launch the application:**
   ```bash
   flyctl launch
   ```
   
   This will use the `fly.toml` configuration file. When prompted:
   - Choose your app name (or use the default)
   - Select your region
   - Don't create a database (use MongoDB Atlas or separate MongoDB app)

4. **Set environment variables:**
   ```bash
   flyctl secrets set MONGODB_URL="your-mongodb-connection-string"
   ```

5. **Deploy the application:**
   ```bash
   flyctl deploy
   ```

6. **Check the deployment status:**
   ```bash
   flyctl status
   flyctl logs
   ```

Your application should now be available at `https://your-app-name.fly.dev`

### Updating the Deployment

To deploy changes:

```bash
flyctl deploy
```

## 🚀 Deployment to Vercel

This application is ready to be deployed to Vercel using the provided configuration.

### Prerequisites

1. Install the Vercel CLI (optional): `npm i -g vercel`
2. Sign up for a Vercel account: https://vercel.com/signup
3. Set up a MongoDB database (MongoDB Atlas recommended)

### Deployment Steps

#### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub** (if not already done)

2. **Import the project in Vercel:**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Vercel will automatically detect the Python project

3. **Configure environment variables:**
   - In the project settings, add the following environment variables:
     - `MONGODB_URL`: Your MongoDB connection string (e.g., `mongodb+srv://username:password@cluster.mongodb.net/todolist_db`)
     - `SECRET_KEY`: A secure secret key for JWT tokens (generate with `openssl rand -hex 32`)

4. **Deploy:**
   - Click "Deploy"
   - Vercel will build and deploy your application

Your application will be available at `https://your-project-name.vercel.app`

#### Option 2: Deploy via Vercel CLI

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Set up environment variables:**
   ```bash
   vercel env add MONGODB_URL
   vercel env add SECRET_KEY
   ```
   
   Enter the values when prompted.

3. **Deploy the application:**
   ```bash
   vercel --prod
   ```

4. **Check the deployment:**
   - Your application will be deployed and the URL will be displayed
   - Visit `https://your-project-name.vercel.app/docs` for API documentation

### Environment Variables Required

- `MONGODB_URL`: MongoDB connection string (e.g., from MongoDB Atlas)
- `SECRET_KEY`: Secret key for JWT token generation

### Notes

- Vercel deploys Python applications as serverless functions
- The application will automatically scale based on demand
- MongoDB Atlas is recommended for the database (free tier available)
- Cold starts may occur on the free tier after periods of inactivity

## 🐳 Docker Deployment

The application includes Docker support for containerized deployment.

### Build and Run with Docker Compose:

```bash
docker-compose up
```

This will start both MongoDB and the backend in containers.

### Build Docker Image Manually:

```bash
docker build -t todolist-backend .
docker run -p 8080:8080 -e MONGODB_URL=mongodb://host.docker.internal:27017 todolist-backend
```

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user profile (requires authentication) |

### Todo Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/todos` | Get all todos |
| GET | `/api/todos?completed=true` | Get completed todos |
| GET | `/api/todos?completed=false` | Get active todos |
| GET | `/api/todos/{id}` | Get todo by ID |
| GET | `/api/todos/search?title={query}` | Search todos by title |
| POST | `/api/todos` | Create new todo |
| PUT | `/api/todos/{id}` | Update todo |
| DELETE | `/api/todos/{id}` | Delete todo |
| DELETE | `/api/todos` | Delete all todos |

### Request/Response Examples

**Create Todo (POST `/api/todos`):**
```json
{
  "title": "Learn FastAPI",
  "description": "Complete the FastAPI tutorial",
  "completed": false
}
```

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

## 🛠️ Technologies Used

### Backend
- **Python 3.11** - Programming language
- **FastAPI** - Modern, fast web framework
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server

### Database
- **MongoDB 7.0+** - NoSQL document database

## 🎨 Key Concepts Demonstrated

### Python Concepts
- **Async/Await**: Asynchronous programming with asyncio
- **Type Hints**: Static typing with Pydantic
- **Dependency Injection**: FastAPI's dependency system
- **Data Validation**: Automatic validation with Pydantic models

### Web Development Concepts
- **RESTful API**: Standard HTTP methods (GET, POST, PUT, DELETE)
- **OpenAPI/Swagger**: Automatic API documentation
- **CORS**: Cross-Origin Resource Sharing configuration
- **HTTP Status Codes**: Proper REST response codes
- **JSON**: Data exchange format
- **MongoDB**: NoSQL database operations (CRUD)

## 📝 Development Notes

- The backend runs on port `8080`
- MongoDB runs on port `27017`
- CORS is configured to allow requests from `http://localhost:5173` (Vite default)
- API documentation is automatically generated and available at `/docs`
- All database operations are asynchronous using Motor

## 🔧 Troubleshooting

**Backend won't start:**
- Check MongoDB is running
- Verify `MONGODB_URL` in `.env` file
- Ensure port 8080 is not in use
- Check Python version (3.11+ required)

**Database connection errors:**
- Verify MongoDB service is running
- Check connection string in `.env`
- Ensure MongoDB is accessible on port 27017

**Import errors:**
- Make sure you're in the virtual environment
- Run `pip install -r requirements.txt` again
- Check Python version compatibility

**Docker issues:**
- Ensure Docker daemon is running
- Check if ports 8080 and 27017 are available
- Try `docker-compose down` and then `docker-compose up` again

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

These provide interactive API documentation where you can test all endpoints.

## 👨‍💻 Author

Created for OOP and Web & Internet courses final project.

## 📄 License

This project is created for educational purposes.
