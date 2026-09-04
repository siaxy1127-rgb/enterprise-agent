from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.agent.agent import run_agent

router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class Source(BaseModel):
    content: str = ""
    source: str = ""
    page: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


class ErrorResponse(BaseModel):
    error: str


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={500: {"model": ErrorResponse}},
)
def chat(request: ChatRequest):
    try:
        result = run_agent(request.question)
        return ChatResponse(
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
        )
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"error": str(exc)},
        )
