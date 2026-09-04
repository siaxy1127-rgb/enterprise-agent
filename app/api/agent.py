from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agent.agent import run_agent

router = APIRouter()


class AgentChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class AgentChatResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/agent/chat", response_model=AgentChatResponse)
def agent_chat(request: AgentChatRequest) -> AgentChatResponse:
    try:
        result = run_agent(request.question)
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent chat failed: {exc}",
        ) from exc

    return AgentChatResponse(
        answer=result["answer"],
        sources=result["sources"],
    )
