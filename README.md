# TaskPilot

## Project Overview

TaskPilot is a **multi-user** task management application built with Python and FastAPI. It provides a secure backend API with **JWT authentication** for creating, managing, and querying tasks, with AI-powered features integrated via providers like OpenRouter. The project is fully containerized using Docker and includes Redis caching for enhanced performance.

## Key Features

- 🔐 **Multi-user support** with JWT authentication
- 📝 **Complete task management** (CRUD operations)
- 🤖 **AI-powered recommendations** and summaries
- 🚀 **Fast and secure** FastAPI backend
- 📦 **Docker containerized** for easy deployment
- ⚡ **Redis caching** for performance
- 📊 **Interactive API documentation** (Swagger UI)
- 🧪 **Comprehensive testing** with pytest
- 🔄 **CI/CD ready** for automated deployment

## Project Architecture

The project is structured with a clear separation of concerns to promote scalability and maintainability:

-   `app/`: Contains all the core application source code.
    -   `api/`: FastAPI routers that define the API endpoints (e.g., `/tasks`, `/agent`).
    -   `services/`: The business logic layer that orchestrates operations (e.g., creating a task, interacting with the AI).
    -   `repositories/`: The data access layer responsible for database interactions.
    -   `models/`: Pydantic models for data validation, serialization, and API specifications.
    -   `core/`: Application configuration management.
    -   `db/`: Database session management.
    -   `cache/`: Redis cache implementation.
-   `data/`: This directory is created automatically to store the persistent SQLite database file (`taskpilot.db`).
-   `docker/`: Contains all files related to containerization.
    -   `Dockerfile`: Defines the recipe for building the production-ready Docker image for the FastAPI app. It's optimized for a small footprint using `python:3.12-alpine`.
    -   `docker-compose.yml`: The orchestrator for defining and running the multi-container Docker application (the `web` API and `redis` cache).
    -   `.env`: **(You must create this file)** Stores environment variables for configuration. See the setup section below.

## Technologies Used

-   **Backend:** Python, FastAPI
-   **Authentication:** JWT (JSON Web Tokens) with bcrypt password hashing
-   **ASGI Server:** Uvicorn
-   **Database:** SQLite with SQLModel (multi-user support)
-   **Caching:** Redis
-   **Containerization:** Docker, Docker Compose
-   **AI Integration:** OpenRouter (configurable providers)
-   **API Documentation:** Automatic Swagger UI generation
-   **Testing:** pytest, pytest-cov, httpx for comprehensive testing
-   **CI/CD:** Ready for GitHub Actions and cloud deployment

---

## 🧪 Testing

TaskPilot includes a solid testing suite covering authentication, task management, AI integration, and health checks.

### Running Tests

**Prerequisites:** Ensure Docker containers are running (`docker-compose up -d`)

```bash
# Navigate to docker directory
cd docker

# Run all tests
docker-compose exec web pytest tests/ -v

# Run tests with coverage report
docker-compose exec web pytest tests/ -v --cov=app

# Run specific test files
docker-compose exec web pytest tests/test_auth_fixed.py -v
docker-compose exec web pytest tests/test_tasks_fixed.py -v
docker-compose exec web pytest tests/test_agent_fixed.py -v
```

### Test Structure
```
tests/
├── test_auth_fixed.py     # Authentication & user management
├── test_tasks_fixed.py    # Task CRUD operations
├── test_agent_fixed.py    # AI integration endpoints
├── test_health_fixed.py   # Health checks
└── conftest.py           # Test configuration
```

The test suite ensures:
- 🔐 **Security**: Users can only access their own data
- 📝 **Functionality**: All CRUD operations work correctly
- 🤖 **AI Integration**: Agent endpoints respond properly
- 🏥 **Health**: Service monitoring works as expected

---

## 🚀 CI/CD & Deployment

TaskPilot is designed for easy deployment with modern CI/CD practices.

### GitHub Actions Ready

The project structure supports automated testing and deployment. Simply add a GitHub Actions workflow file to automatically:
- Run tests on every push
- Build Docker containers
- Deploy to production on merge to main

### Render.com Deployment (Recommended)

1. **Fork this repository**
2. **Connect to Render.com**
3. **Create a Web Service** from your GitHub repo
4. **Set environment variables** in Render dashboard
5. **Deploy automatically** - uses included `render.yaml`

### Manual Deployment

```bash
# Build and run production image
docker build -t taskpilot:latest .
docker run -p 8000:8000 --env-file .env taskpilot:latest
```

**Production Environment Variables:**
- `SECRET_KEY` - Strong secret for app security
- `JWT_SECRET_KEY` - JWT token signing key  
- `AI_API_KEY` - Your OpenRouter API key
- `REDIS_PASSWORD` - Secure Redis password
- `DEBUG=false` - Disable debug mode

---

## How to Run the Project

### Step 1: Prerequisites

-   Ensure you have **Docker Desktop** installed and running on your system.

### Step 2: Configure Environment Variables

Create a `.env` file in the `docker/` directory with your configuration:

```env
# Security (REQUIRED - Generate with: openssl rand -hex 32)
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration (REQUIRED for AI features)
AI_PROVIDER=openrouter
AI_API_KEY=your-openrouter-api-key-here

# Redis Configuration (works with docker-compose)
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password-here
REDIS_DB=0

# Database (SQLite in Docker volume)
DATABASE_URL=sqlite:///./data/taskpilot.db

# App Settings
APP_NAME=TaskPilot
DEBUG=false
```

**Important:** 
- Replace `SECRET_KEY` and `JWT_SECRET_KEY` with random strings (use `openssl rand -hex 32`)
- Add your OpenRouter API key for AI features
- Set a strong Redis password for security

### Step 3: Build and Run the Application

All the following commands must be run from within the `docker/` directory.

-   **To build and start the services:**
    This is the main command to start or resume your application. It builds the images if they don't exist and starts the `web` and `redis` containers in the background (`-d`). If the containers are already running, it will gracefully recreate only the ones that have changed.
    ```bash
    docker-compose up --build -d
    ```

-   **To view the application logs:**
    This is essential for debugging. It will "follow" (`-f`) the real-time logs of the `web` service. Press `Ctrl+C` to stop viewing.
    ```bash
    docker-compose logs -f web
    ```

-   **To stop the application:**
    This command stops and removes the containers. Your data in the database and Redis cache will be preserved in Docker volumes.
    ```bash
    docker-compose down
    ```

-   **To resume the application:**
    If you have previously stopped the application and want to start it again without rebuilding, use this command. It will start the existing containers without rebuilding them.
    ```bash
    docker-compose up -d
    ```

-   **To stop the application AND remove all data:**
    **Warning:** This will permanently delete the SQLite database and Redis cache.
    ```bash
    docker-compose down -v
    ```

### Step 4: Access the Application

Once the containers are running:

-   **API Documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

### Step 5: Authentication & Usage

TaskPilot requires user registration and authentication:

**1. Register a new user:**
```bash
curl -X POST "http://localhost:8000/api/users/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "myuser", "email": "user@example.com", "password": "password123"}'
```

**2. Login to get an access token:**
```bash
curl -X POST "http://localhost:8000/api/users/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=myuser&password=password123"
```

**3. Use the token for authenticated requests:**
```bash
curl -X POST "http://localhost:8000/api/tasks/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Complete project documentation", 
       "description": "Update README with multi-user features",
       "due_date": "2025-06-25T10:00:00",
       "priority": "high",
       "tags": ["documentation", "urgent"],
       "mini_tasks": {"Review content": false, "Add examples": false}
     }'
```

**Available Endpoints:**
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login (returns JWT token) 
- `GET /api/tasks/` - Get all user's tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `GET /api/agent/summary` - AI project summary
- `GET /api/agent/recommendations` - AI task recommendations

---

## Security & Deployment Notes

- **✅ Safe to commit:** All configuration files in this repository are safe to push to Git
- **❌ Never commit:** The `.env` file contains secrets and is in `.gitignore`
- **🔐 Production:** Use strong, unique values for all secret keys and passwords
- **🌐 Multi-user:** Each user's tasks are isolated and secured with JWT authentication

---

## Project Status & Next Steps

TaskPilot is a complete, production-ready multi-user task management API with:
- ✅ Secure user authentication (JWT)
- ✅ Complete task CRUD operations  
- ✅ AI-powered features
- ✅ Docker containerization
- ✅ Redis caching
- ✅ Multi-user data isolation

**Potential enhancements:**
- Frontend web interface (React/Vue)
- Real-time notifications (WebSockets)
- Advanced AI integrations
- Team collaboration features
- Mobile app (React Native/Flutter)
