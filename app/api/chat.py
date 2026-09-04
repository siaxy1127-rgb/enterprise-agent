from operator import itemgetter

from fastapi import APIRouter, HTTPException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field

from app.models.llm import get_llm
from app.rag.vectorstore import get_retriever

router = APIRouter()

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是企业知识库助手。请仅根据下列上下文回答用户问题。"
            "若上下文中没有相关信息，请明确说明不知道，不要编造。\n\n"
            "上下文：\n{context}",
        ),
        ("human", "{question}"),
    ]
)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


def _format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    """Build a standard LCEL RAG chain (no Agent)."""
    retriever = get_retriever()
    llm = get_llm()

    return (
        RunnablePassthrough.assign(
            docs=itemgetter("question") | retriever,
        )
        .assign(
            context=lambda x: _format_docs(x["docs"]),
        )
        .assign(
            answer=(
                {
                    "context": itemgetter("context"),
                    "question": itemgetter("question"),
                }
                | PROMPT
                | llm
                | StrOutputParser()
            ),
        )
    )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = build_rag_chain().invoke(
            {"question": request.question}
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"RAG chat failed: {exc}",
        ) from exc

    sources = [doc.page_content for doc in result["docs"]]

    return ChatResponse(
        answer=result["answer"],
        sources=sources,
    )
