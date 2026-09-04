from fastapi import FastAPI

from app.api.agent import router as agent_router
from app.api.chat import router as chat_router
from app.api.routes import router as api_router
from app.api.upload import router as upload_router

app = FastAPI(title="Enterprise Knowledge Agent")

app.include_router(api_router)

app.include_router(
    upload_router,
    prefix="/api",
)

app.include_router(
    chat_router,
    prefix="/api",
)

app.include_router(
    agent_router,
    prefix="/api",
)


@app.get("/")
def root():
    return {
        "message": "Enterprise Agent is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
