from langchain_chroma import Chroma

from app.models.embedding import get_embedding
from app.core.config import settings


COLLECTION_NAME = "enterprise_kb"


def create_vectorstore(chunks, embedding=None):
    """
    创建 Chroma 向量数据库
    """

    if embedding is None:
        embedding = get_embedding()


    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=str(settings.chroma_path),
        collection_name=COLLECTION_NAME,
    )


    return vectorstore



def get_vectorstore(embedding=None):
    """
    加载已有 Chroma
    """

    if embedding is None:
        embedding = get_embedding()


    return Chroma(
        persist_directory=str(settings.chroma_path),
        embedding_function=embedding,
        collection_name=COLLECTION_NAME,
    )



def load_vectorstore(embedding=None):

    return get_vectorstore(embedding)



def get_retriever(vectorstore=None):

    if vectorstore is None:
        vectorstore = get_vectorstore()


    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k":1
        }
    )



def save_to_chroma(chunks, embedding=None):

    return create_vectorstore(
        chunks,
        embedding
    )