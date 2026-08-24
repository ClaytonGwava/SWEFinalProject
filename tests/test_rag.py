from unittest.mock import patch

from app.services import rag_service


def test_search_documents_returns_relevant_documents():

    fake_documents = [
        type(
            "Document",
            (),
            {
                "page_content": "Software engineering is a systematic approach to software development.",
                "metadata": {
                    "source": "software_engineering.pdf",
                    "page": 5
                }
            }
        )()
    ]

    with patch(
        "app.services.rag_service.load_vector_store"
    ) as mock_load_store:

        mock_vector_store = mock_load_store.return_value

        mock_vector_store.similarity_search.return_value = (
            fake_documents
        )

        results = rag_service.search_documents(
            "What is software engineering?",
            1
        )

        mock_vector_store.similarity_search.assert_called_once_with(
            "What is software engineering?",
            k=4
        )

        assert len(results) == 1

        assert (
            results[0].page_content ==
            "Software engineering is a systematic approach to software development."
        )

        assert (
            results[0].metadata["source"] ==
            "software_engineering.pdf"
        )