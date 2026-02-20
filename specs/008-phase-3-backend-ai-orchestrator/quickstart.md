# Quickstart Guide: Phase 3 Backend AI Orchestrator

This guide provides instructions to quickly set up, configure, and run the Phase 3 Backend AI Orchestrator service.

## Prerequisites

-   Python 3.10+
-   `pip` (Python package installer)
-   Access to a Neon PostgreSQL database (connection string required)
-   OpenAI API Key (for OpenAI Agents SDK)
-   MCP SDK credentials (if applicable)

## 1. Setup Environment

1.  **Navigate to the `phase-3` directory**:
    ```bash
    cd phase-3
    ```

2.  **Create a Python virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 2. Configuration

Create a `.env` file in the `phase-3` directory. This file will store your sensitive environment variables.

Example `.env` file (`phase-3/.env`):
```
DATABASE_URL="postgresql+asyncpg://user:password@host:port/dbname" # Replace with your actual Neon DB URL
OPENAI_API_KEY="your_openai_api_key_here" # Replace with your OpenAI API Key
# MCP_SDK_CLIENT_ID="your_mcp_client_id" # Uncomment and replace if using MCP SDK with client credentials
# MCP_SDK_CLIENT_SECRET="your_mcp_client_secret" # Uncomment and replace if using MCP SDK with client credentials
```
**IMPORTANT**: Replace the placeholder values with your actual credentials. For `DATABASE_URL`, ensure it's a valid connection string to your Neon PostgreSQL database.

## 3. Database Migrations

Apply the database migrations to set up the `conversations` and `messages` tables, and ensure compatibility with the existing `tasks` table.

```bash
cd phase-3
source venv/bin/activate
alembic upgrade head
```

## 4. Run the FastAPI Server

Start the FastAPI application using `uvicorn` from the `phase-3` directory:

```bash
cd phase-3
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```
The API will be accessible at `http://localhost:8000`.

## 5. Basic API Interaction (using `curl`)

Replace `{user_id}` with a valid UUID.

### Send a message to the AI agent (starts a new conversation)

```bash
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "message": "Hello, what is the capital of France?"
         }'
```

### Continue an existing conversation

```bash
curl -X POST "http://localhost:8000/api/{user_id}/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "conversation_id": "your_conversation_id_here",
           "message": "And what about Germany?"
         }'
```
Replace `your_conversation_id_here` with the `conversation_id` received from a previous response.

### Add a new task

```bash
curl -X POST "http://localhost:8000/api/tasks/{user_id}/add" \
     -H "Content-Type: application/json" \
     -d '{
           "description": "Buy groceries",
           "due_date": "2026-02-15T18:00:00Z"
         }'
```

### List tasks

```bash
curl -X GET "http://localhost:8000/api/tasks/{user_id}/list"
```

### Complete a task

```bash
curl -X POST "http://localhost:8000/api/tasks/{user_id}/complete/{task_id}"
```
Replace `{task_id}` with the ID of the task to complete.

### Update a task

```bash
curl -X PUT "http://localhost:8000/api/tasks/{user_id}/update/{task_id}" \
     -H "Content-Type: application/json" \
     -d '{
           "description": "Buy organic groceries",
           "status": "in_progress"
         }'
```
Replace `{task_id}` with the ID of the task to update.

### Delete a task

```bash
curl -X DELETE "http://localhost:8000/api/tasks/{user_id}/delete/{task_id}"
```
Replace `{task_id}` with the ID of the task to delete.
