import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.document_service import load_document

load_dotenv()

VECTOR_STORE_PATH = "vector_store"


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


def create_vector_store(file_path: str):
    """
    Load a document, split it into chunks,
    create embeddings and store them in FAISS.
    """

    documents = load_document(file_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local(
        VECTOR_STORE_PATH
    )

    return len(chunks)


def load_vector_store():
    """
    Load the existing FAISS vector store.
    """

    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(
            "Vector store does not exist. "
            "Upload and process a document first."
        )

    return FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def search_documents(
    question: str,
    k: int = 4
):
    """
    Search the vector store for documents
    relevant to the student's question.
    """

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results