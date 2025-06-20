# TaskPilot

## Project Overview

TaskPilot is a task management application built with Python and FastAPI. It provides a robust backend API for creating, managing, and querying tasks, with AI-powered features integrated via providers like OpenRouter. The project is fully containerized using Docker and Docker Compose, ensuring a consistent and reproducible environment for both development and production. It utilizes a Redis cache to enhance performance for frequent requests.

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
-   **ASGI Server:** Uvicorn
-   **Caching:** Redis
-   **Containerization:** Docker, Docker Compose
-   **Database:** SQLite (persisted via a Docker volume)
-  **AI Integration:** OpenRouter (or other providers as configured)
-   **Logging:** Standard Python logging with FastAPI integration

---

## How to Run the Project

### Step 1: Prerequisites

-   Ensure you have **Docker Desktop** installed and running on your system.

### Step 2: Create and Configure the Environment File (`.env`)

The application's behavior is controlled by environment variables. You **must** create a file named `.env` inside the `docker/` directory to store these settings and secrets. This file is the control panel for the application.

#### Detailed Explanation of Each Variable

Here is a line-by-line breakdown of every setting you need to configure in your `.env` file. **Do not commit this file to Git.**

-   `SECRET_KEY`
    -   **Purpose:** This is a critical security key. The application uses it to sign and verify tokens (like for password resets or API authentication). It ensures that data is not tampered with.
    -   **Action:** You **must** replace the default value with a long, random, and unpredictable string. A compromised key could lead to major security vulnerabilities.
    -   **How to Generate:** Run `openssl rand -hex 32` in your terminal to generate a strong key.

-   `AI_PROVIDER`
    -   **Purpose:** Defines which AI service the application should connect to. The code is set up to use `openrouter` by default.
    -   **Action:** For now, leave this as `openrouter`.

-   `AI_API_KEY`
    -   **Purpose:** This is your personal API key for the AI provider you specified above. It's a secret password that gives you access to the AI service.
    -   **Action:** You **must** replace the placeholder with your actual API key from OpenRouter (or another provider).

-   `REDIS_HOST`
    -   **Purpose:** Tells the FastAPI application the hostname of the Redis cache server. In our `docker-compose.yml`, the Redis service is named `redis`.
    -   **Action:** Do not change this value. It is set to `redis` so the `web` container can find the `redis` container on Docker's internal network.

-   `REDIS_PORT`
    -   **Purpose:** The port that Redis uses to listen for connections inside the Docker network.
    -   **Action:** Do not change this value. The standard Redis port is `6379`.

-   `REDIS_PASSWORD`
    -   **Purpose:** A password to protect your Redis cache. While optional, it is **highly recommended** for security, especially in production.
    -   **Action:** Set a strong, unique password here. The `docker-compose.yml` file is configured to pass this password to both the Redis server and the FastAPI application.

-   `REDIS_DB`
    -   **Purpose:** Redis can maintain multiple databases, identified by a number. `0` is the default database.
    -   **Action:** You can leave this as `0` unless you have a specific reason to use a different database index.

-   `DATABASE_URL`
    -   **Purpose:** This is the connection string for the application's database. It tells FastAPI where to find and how to connect to the database.
    -   **Action:** Do not change this value. It is pre-configured to use the `taskpilot.db` SQLite file located in the `/app/data` directory inside the container, which is persisted to your local machine via a Docker volume.

-   `APP_NAME`
    -   **Purpose:** Sets the name of the application, which might be used in API responses or logs.
    -   **Action:** You can leave this as `TaskPilot` or change it if you wish.

-   `DEBUG`
    -   **Purpose:** Toggles FastAPI's debug mode.
    -   **Action:** Set to `false` for production. Setting it to `true` will expose detailed error information, which is useful for development but a security risk in a live environment.

#### Complete `.env` Example Template

Navigate to the `docker/` directory, create a file named `.env`, and paste the following content into it. Then, fill in your secret values.

```env
# ------------------------------------------------------------------
#        TaskPilot Environment Configuration (.env)
# ------------------------------------------------------------------
# This file contains all the necessary configuration and secrets
# for the application. Create this file inside the 'docker/' directory.
# ------------------------------------------------------------------

# --- Security ---
# A strong, random string used for security functions (e.g., signing tokens).
# It's critical that this is kept secret and is a long, unpredictable string.
# You can generate a new one by running this command in your terminal:
# openssl rand -hex 32
SECRET_KEY=d8e6a0b4c1e8f2d7a9c3b5d1f0e9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1

# --- AI Configuration ---
# Specifies which AI service to use. The application is configured to work
# with 'openrouter' by default, but could be extended for others like 'openai'.
AI_PROVIDER=openrouter

# Your personal API key from the AI provider specified above.
# This is a secret and should be treated like a password.
# The format will vary by provider.
AI_API_KEY=sk-or-v1-abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234

# --- Redis Cache Configuration ---
# These variables configure the connection to the Redis cache service.
# In the Docker environment, you should not need to change these values.

# The hostname for the Redis container on the internal Docker network.
# 'redis' is the service name defined in docker-compose.yml.
REDIS_HOST=redis

# The port that the Redis server listens on inside the network.
REDIS_PORT=6379

# An optional password for connecting to Redis. It is highly recommended
# to set a strong password in a production environment.
REDIS_PASSWORD=a-very-strong-redis-password-123!

# The Redis database instance to use. '0' is the default.
REDIS_DB=0

# --- Database Configuration ---
# The connection string for the database.
# This is pre-configured for the SQLite database running inside a Docker volume
# and should not be changed unless you are re-architecting the database setup.
DATABASE_URL=sqlite:///./data/taskpilot.db

# --- General Application Settings ---
# The public name of the application.
APP_NAME=TaskPilot

# Toggles debug mode.
# 'false' is the standard for production.
# 'true' will provide more verbose error messages, but can be a security risk.
DEBUG=false
```

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

### Step 4: Verify and Access the Application

Once the containers are running, you can verify that everything is working correctly.

-   **API Documentation (Swagger UI):**
    The best way to explore all available API endpoints is through the interactive Swagger UI documentation. Open this URL in your browser:
    [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 5: Example API Usage (Creating a Task)

Here is a quick example of how to create a new task using `curl` from your terminal. This demonstrates a basic interaction with the API.

```bash
curl -X 'POST' \
  'http://localhost:8000/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Finalize the project README",
  "description": "Review and update the README.md file with complete setup and usage instructions.",
  "due_date": "2025-06-21T10:00:00Z"
}'
```

If successful, the API will respond with the details of the newly created task, including its ID.

---

## Project Status & Future Improvements

This project provides a solid foundation for a task management application. The core API is functional, containerized, and includes caching.

Potential next steps could include:
-   **Adding User Authentication:** Implementing OAuth2 to secure endpoints.
-   **Implementing a Test Suite:** Adding unit and integration tests using `pytest`.
-   **CI/CD Pipeline:** Setting up a pipeline (e.g., with GitHub Actions) to automate testing and deployment.
-   **Adding Linting and Formatting:** Integrating tools like `Ruff` and `Black` to ensure code quality.
