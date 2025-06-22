# TaskPilot
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](#testing)

## Overview
TaskPilot is a modern multi-user task management backend built with Python and FastAPI. It features secure JWT-based authentication, robust task CRUD operations, and advanced AI-driven capabilities powered by OpenRouter. The entire system is containerized using Docker, leverages Redis caching for optimal performance, and is fully prepared for CI/CD deployment.

## Key Features
- 🔐 Secure multi-user authentication with JWT tokens and password hashing
- 📝 Comprehensive task management (create, read, update, delete)
- 🤖 AI-powered summaries and recommendations integrated via configurable providers
- 🚀 FastAPI backend delivering high performance and easy scalability
- ⚡ Redis caching for improved response times and resource efficiency
- 📦 Containerized with Docker and Docker Compose for seamless deployment
- 🧪 Extensive automated tests with pytest to ensure reliability
- 🔄 CI/CD pipeline integration ready for GitHub Actions and Render.com
- 📊 Interactive API docs automatically generated with Swagger UI

## Project Architecture
```
TaskPilot/
├── app/                # Core application logic and modules
├── api/                # FastAPI routers defining API endpoints
├── services/           # Business logic layer (e.g., AI integration, task processing)
├── repositories/       # Data access layer for database interactions
├── models/             # Pydantic models for data validation and serialization
├── core/               # Configuration and settings management
├── db/                 # Database session and migrations
├── cache/              # Redis caching logic
├── docker/             # Dockerfile, docker-compose, and deployment configs
├── tests/              # Unit and integration tests
└── data/               # Persistent SQLite database files
```

## Technologies
- **Backend:** Python 3.12, FastAPI
- **Authentication:** JWT tokens, bcrypt password hashing
- **Server:** Uvicorn ASGI server
- **Database:** SQLite with SQLModel ORM
- **Cache:** Redis
- **Containerization:** Docker, Docker Compose
- **AI:** OpenRouter (configurable AI provider)
- **Testing:** pytest, pytest-cov, httpx
- **CI/CD:** GitHub Actions workflow, Render.com deployment
- **API Docs:** Swagger UI auto-generated

## Setup & Usage

### Prerequisites
- Docker Desktop installed and running
- An OpenRouter API key (for AI features)
- Basic familiarity with command line

### Environment Variables (docker/.env)
Create a `.env` file with your configuration:

```env
SECRET_KEY=your-random-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

AI_PROVIDER=openrouter
AI_API_KEY=your-openrouter-api-key

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_DB=0

DATABASE_URL=sqlite:///./data/taskpilot.db

APP_NAME=TaskPilot
DEBUG=false
```

**Note:** Generate secure random keys with `openssl rand -hex 32`

### Running the Application
```bash
cd docker
docker-compose up --build -d
```

To check logs:
```bash
docker-compose logs -f web
```

To stop:
```bash
docker-compose down
```

### Access
- **API docs:** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

## Authentication & API Endpoints

**Register:**
```bash
curl -X POST "http://localhost:8000/api/users/register" \
-H "Content-Type: application/json" \
-d '{"username":"myuser","email":"user@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/users/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=myuser&password=password123"
```

**Use token for authorized calls:**
```bash
curl -X POST "http://localhost:8000/api/tasks/" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Finish README","description":"Improve project README","due_date":"2025-06-25T10:00:00","priority":"high"}'
```

### Main Endpoints
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - User login (returns JWT)
- `GET /api/tasks/` - List user's tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `GET /api/agent/summary` - AI-generated project summary
- `GET /api/agent/recommendations` - AI task recommendations

## Testing
Run tests inside Docker container:
```bash
docker-compose exec web pytest tests/ -v --cov=app
```

Test suite covers:
- User authentication
- Task CRUD operations
- AI integration endpoints
- Health monitoring

## CI/CD & Deployment
- Fully configured GitHub Actions pipeline runs tests, security scans, and builds Docker images on every push.
- Automatically deploys to Render.com when merging to main.
- Render uses `render.yaml` to orchestrate services (web + Redis).
- Easy to extend for staging and production environments.

## Future Improvements
- Add React or Vue frontend for a full user interface
- Implement real-time notifications with WebSockets
- Enhance AI capabilities with more providers and features
- Support team collaboration and task assignments
- Develop mobile apps (React Native / Flutter)

## Contact
Created by Roee Shlosberg — bioinformatics student and software developer passionate about building scalable backend APIs with AI integration.
