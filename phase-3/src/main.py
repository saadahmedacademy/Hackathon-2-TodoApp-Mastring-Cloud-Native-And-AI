from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.api.v1.endpoints import chat
from src.utils.error_handlers import register_exception_handlers
from src.config import settings
from src.models.conversation import Conversation  # registers in SQLModel metadata
from src.models.message import Message            # registers in SQLModel metadata
# Note: src.models.todo is imported via MCP tools — the 'todo' table is owned
# by Phase-2 and must NOT be auto-created here. Use Alembic migrations only.


app = FastAPI(title="Phase 3 Backend AI Orchestrator")

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "https://hk-2-project.vercel.app/",
    settings.FRONTEND_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)

register_exception_handlers(app)


@app.get("/")
async def root():
    return {"message": "Phase 3 Backend AI Orchestrator is running!"}
