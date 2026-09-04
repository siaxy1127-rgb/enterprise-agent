from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vectorstore import save_to_chroma
from app.models.embedding import get_embedding


def process_pdf(file_path):

    # 1. PDF Loader

    documents = load_pdf(file_path)

    print(
        f"Loaded pages: {len(documents)}"
    )


    # 2. Text Splitter

    chunks = split_documents(documents)

    print(
        f"Created chunks: {len(chunks)}"
    )


    # 3. Embedding

    embedding = get_embedding()


    # 4. ChromaDB

    db = save_to_chroma(
        chunks,
        embedding
    )


    return db