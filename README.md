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
- **Database Migrations on Startup**: Alembic migrations execute automatically via an `entrypoint.sh` script before the API container fully starts, replacing the need for a separate migration container while guaranteeing schema validity.
- **Role-Based Access Control (Admin Features)**: The system includes role-based access control with an Administrator role capable of managing users and overseeing all tasks across the platform.

## Database Schema

```
┌─────────────────────────┐       ┌─────────────────────────┐
│         users           │       │         tasks           │
├─────────────────────────┤       ├─────────────────────────┤
│ id          PK  int     │──┐    │ id          PK  int     │
│ email       UQ  varchar │  │    │ title           varchar │
│ password        varchar │  ├───<│ user_id     FK  int     │
│ role            varchar │  │    │ status          varchar │
│ created_at      timestamp│  │    │ created_at      timestamp│
└─────────────────────────┘  │    └─────────────────────────┘
                             │
                             │    ┌──────────────────────────┐
                             │    │     refresh_tokens       │
                             │    ├──────────────────────────┤
                             │    │ id          PK  int      │
                             │    │ token       UQ  varchar  │
                             └───<│ user_id     FK  int      │
                                  │ expires_at      timestamp│
                                  │ created_at      timestamp│
                                  └──────────────────────────┘
```

- **users**: Stores account credentials and roles (`user` or `admin`). One user can own many tasks and refresh tokens (cascade delete).
- **tasks**: Each task belongs to a user via `user_id`. Status is one of `todo`, `doing`, or `done`.
- **refresh_tokens**: Tracks JWT refresh tokens per user for token rotation and revocation.

## Default Accounts
A default admin account is seeded automatically upon applying database migrations:
- **Email**: `admin@gmail.com`
- **Password**: `Admin@123`
- **Role**: `admin`

## How to Run the Project

### 1. Running with Docker Compose (Recommended)
The easiest way to get the project up and running is by using Docker Compose. This will spin up both the FastAPI application and the PostgreSQL database.

1. **Environment Setup**:
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. **Start the Application (Development)**:
   This uses the dev compose file which mounts your local code for hot-reloading:
   ```bash
   docker compose -f docker-compose.development.yml up -d --build
   ```
3. **Start the Application (Production)**:
   For production deployment (without hot-reloading):
   ```bash
   docker compose up -d --build
   ```

*Note: Database migrations are applied automatically when the API container starts.*

### 2. Running Locally (Without Docker)
If you prefer to run the Python application directly on your host machine:

1. **Start a local PostgreSQL instance** and ensure your `.env` is configured to point to it (e.g., `POSTGRES_SERVER=localhost`).
2. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   poetry install
   ```
3. **Run Database Migrations** physically:
   ```bash
   alembic upgrade head
   ```
4. **Start the FastAPI server**:
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

# Admin Default Accounts
ADMIN_EMAIL=admin_prod@yourdomain.com
ADMIN_PASSWORD=str0ng_adm1n_p@ssw0rd

# Set environment
ENVIRONMENT=production
```
*Note: Make sure `docker-compose.override.yml` is removed or ignored in the production environment.*
