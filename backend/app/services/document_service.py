from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader
)


def load_document(file_path: str):
    """
    Load a PDF, DOCX, or PPTX document
    and return LangChain Document objects.
    """

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))

    elif extension == ".docx":
        loader = Docx2txtLoader(str(path))

    elif extension == ".pptx":
        loader = UnstructuredPowerPointLoader(str(path))

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    return loader.load()