import os

from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from app.services.document_service import load_document

load_dotenv()

VECTOR_STORE_BASE_PATH = "vector_store"


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


def get_course_vector_path(course_id: int):
    """
    Return the vector store path for a course.
    """

    return os.path.join(
        VECTOR_STORE_BASE_PATH,
        f"course_{course_id}"
    )


def create_vector_store(
    file_path: str,
    course_id: int
):
    """
    Add a document to the course-specific
    FAISS vector store.
    """

    documents = load_document(
        file_path
    )

    text_splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    )

    chunks = text_splitter.split_documents(
        documents
    )

    vector_store_path = (
        get_course_vector_path(
            course_id
        )
    )

    os.makedirs(
        vector_store_path,
        exist_ok=True
    )

    # Check whether a course vector store
    # already exists.
    index_file = os.path.join(
        vector_store_path,
        "index.faiss"
    )

    if os.path.exists(index_file):

        vector_store = FAISS.load_local(
            vector_store_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        vector_store.add_documents(
            chunks
        )

    else:

        vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )

    vector_store.save_local(
        vector_store_path
    )

    return len(chunks)

def load_vector_store(course_id: int):
    """
    Load the FAISS vector store belonging
    to a specific course.
    """

    vector_store_path = get_course_vector_path(
        course_id
    )

    if not os.path.exists(
        vector_store_path
    ):
        raise FileNotFoundError(
            "Vector store does not exist for "
            f"course {course_id}. "
            "Upload and process a document first."
        )

    return FAISS.load_local(
        vector_store_path,
        embeddings,
        allow_dangerous_deserialization=True
    )


def search_documents(
    question: str,
    course_id: int,
    k: int = 4
):
    """
    Search only the vector store belonging
    to the selected course.
    """

    vector_store = load_vector_store(
        course_id
    )

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results