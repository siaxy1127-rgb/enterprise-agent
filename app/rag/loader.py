from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)


def load_pdf(file_path: str):
    """
    Load PDF document.

    Args:
        file_path:
            PDF file path

    Returns:
        List[Document]
    """

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    # 清洗 metadata
    for doc in documents:
        doc.metadata = {
            "source": file_path,
            "page": doc.metadata.get("page", 0),
        }

    return documents



def load_txt(file_path: str):
    """
    Load txt document.

    Args:
        file_path:
            txt file path

    Returns:
        List[Document]
    """

    loader = TextLoader(
        file_path,
        encoding="utf-8"
    )

    documents = loader.load()


    for doc in documents:
        doc.metadata = {
            "source": file_path
        }


    return documents



def load_document(file_path: str):
    """
    Load a single document according to file type.
    """

    path = Path(file_path)

    suffix = path.suffix.lower()


    if suffix == ".pdf":

        return load_pdf(file_path)


    elif suffix == ".txt":

        return load_txt(file_path)


    else:

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )



def load_documents(directory: str):
    """
    Load all supported documents from directory.

    Supported:
        - pdf
        - txt
    """

    documents = []

    directory_path = Path(directory)


    for file in directory_path.rglob("*"):

        if not file.is_file():
            continue


        if file.suffix.lower() in [
            ".pdf",
            ".txt"
        ]:

            docs = load_document(
                str(file)
            )

            documents.extend(docs)


    return documents