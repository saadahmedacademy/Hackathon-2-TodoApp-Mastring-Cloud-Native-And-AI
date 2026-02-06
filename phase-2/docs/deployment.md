# Deployment Documentation: Todo API

## Overview

This document provides instructions for deploying the Todo API in various environments.

## Prerequisites

- Python 3.11+
- Pip package manager
- Access to a PostgreSQL database (for production) or ability to run SQLite (for development)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd phase-2
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Required environment variables:

- `DATABASE_URL`: Database connection string (e.g., `postgresql://user:password@localhost/dbname` or `sqlite:///./todo.db`)
- `SECRET_KEY`: Secret key for JWT tokens (generate a strong random key for production)
- `DEBUG`: Set to `True` for development, `False` for production

## Running the Application

### Development

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn src.api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

Or using a process manager like systemd or supervisord:

```bash
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Database Setup

### Using Alembic for Migrations

1. Initialize the database:

```bash
alembic upgrade head
```

2. To create new migrations:

```bash
alembic revision --autogenerate -m "Migration message"
alembic upgrade head
```

### Direct SQLModel Table Creation

If not using Alembic, tables will be created automatically on startup via the event handler in `src/api/main.py`.

## API Endpoints

All endpoints require a `user_id` in the path for multi-user isolation:

- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks` - List all tasks for user
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update completion status
- `GET /health` - Health check

## Environment-Specific Configurations

### Development

- Set `DEBUG=True`
- Use SQLite database for simplicity
- Enable auto-reload with `--reload` flag

### Staging

- Use a dedicated PostgreSQL database
- Set `DEBUG=False`
- Use multiple workers for performance testing

### Production

- Use a production-grade PostgreSQL database with backups
- Set `DEBUG=False`
- Use a reverse proxy (nginx) with SSL
- Monitor application logs
- Set up automated backups
- Use environment variables for secrets

## Security Considerations

- Never expose the application directly to the internet without a reverse proxy
- Use HTTPS in production
- Rotate the `SECRET_KEY` periodically
- Validate and sanitize all user inputs
- Implement rate limiting for API endpoints
- Regularly update dependencies

## Monitoring and Logging

The application logs important events including:
- Request/response details
- Error conditions
- Database operations

Configure your deployment platform to collect and analyze these logs.

## Scaling

The application supports horizontal scaling behind a load balancer. Ensure:
- Sticky sessions are disabled (stateless API)
- Database can handle increased connection load
- Shared caching layer if implemented
- Proper database connection pooling

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Verify `DATABASE_URL` is correct and database is accessible
2. **Port Already in Use**: Change the port number in the uvicorn command
3. **Permission Errors**: Ensure the application has write access to the working directory
4. **Missing Dependencies**: Run `pip install -r requirements.txt` again

### Health Checks

Use the `/health` endpoint to check application status.