# Task Management API

A Task Management RESTful API built with FastAPI, SQLAlchemy (async), and PostgreSQL.
Includes JWT authentication, role-based access control, rate limiting, and structured logging.

## Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (with asyncpg)
- **ORM**: SQLAlchemy 2.0 (async methods)
- **Migrations**: Alembic
- **Auth**: JWT (JSON Web Tokens), bcrypt for password hashing
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Design Decisions
- **Async-First Approach**: Utilized FastAPI, asyncpg, and SQLAlchemy 2.0 for non-blocking I/O, ensuring high throughput and concurrency.
- **Layered Architecture**: The codebase is separated into distinct layers: routers (API entrypoints), services (business logic), repositories (data access), and schemas (Pydantic validation). This separation of concerns improves maintainability and testability.
- **Stateless Authentication**: Chose JWT with short-lived access tokens and longer-lived refresh tokens instead of session-based auth to ensure scalability.
- **Decoupled Database Migrations**: Alembic runs in its own ephemeral Docker container (`migrate`) to ensure schema changes are applied before the API service boots up safely.

## Database Setup Instructions
1. **Prerequisites**: Ensure you have PostgreSQL installed locally or use the provided Docker setup.
2. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your database credentials:
   ```dotenv
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_SERVER=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=taskdb
   ```
3. **Running Migrations**:
   If running locally (without Docker), apply migrations using Alembic:
   ```bash
   alembic upgrade head
   ```
   *Note: When using Docker Compose, migrations are applied automatically on startup.*

## How to Run the Project

### Local Development with Docker Dev Environment
If you want to run the development environment utilizing the specific development docker-compose file:
1. Ensure your `.env` file is set up.
2. Run the following command to start the stack using `docker-compose.development.yml`:
   ```bash
   docker-compose -f docker-compose.development.yml up -d --build
   ```
   This setup mounts your local configs and binds via the `env_file` mapping configured in the development setup.

### Local Development Setup
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt # or 'poetry install' if using Poetry
   ```
2. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Testing
Run automated tests locally with Pytest:
```bash
PYTHONPATH=. pytest
```
Or run with coverage:
```bash
PYTHONPATH=. pytest --cov=app --cov-report=term-missing
```

## API Documentation
Once the API is running, you can access the automatically generated interactive documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) (Best for testing endpoints directly)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) (Detailed and structured documentation)

## Production Deployment
For production, ensure your `.env` is configured securely:
```dotenv
# Use a production-grade database URL
POSTGRES_USER=strong_username
POSTGRES_PASSWORD=very_strong_password
POSTGRES_SERVER=db
POSTGRES_DB=taskdb

# Security settings
SECRET_KEY=generate_a_secure_32_byte_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Set environment
ENVIRONMENT=production
```
*Note: Make sure `docker-compose.override.yml` is removed or ignored in the production environment.*
