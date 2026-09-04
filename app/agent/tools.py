import json

from langchain_core.tools import tool

from app.rag.vectorstore import get_retriever


@tool
def knowledge_search(query: str) -> str:
    """
    Search the enterprise knowledge base.

    Use this tool when the user asks about:
    - company policies
    - employee rules
    - internal procedures
    - enterprise documents

    Returns relevant documents with source information.
    """

    retriever = get_retriever()

    docs = retriever.invoke(query)


    if not docs:
        return json.dumps(
            {
                "results": []
            },
            ensure_ascii=False
        )


    results = []


    for doc in docs:

        metadata = doc.metadata


        # LangChain PDF page 从0开始
        page = metadata.get("page")

        if page is not None:
            page = page + 1


        results.append(
            {
                "content": doc.page_content.strip(),

                "source": metadata.get(
                    "source",
                    "unknown"
                ),

                "page": page
            }
        )


    return json.dumps(
        {
            "results": results
        },
        ensure_ascii=False,
        indent=2
    )


TOOLS = [
    knowledge_search
]