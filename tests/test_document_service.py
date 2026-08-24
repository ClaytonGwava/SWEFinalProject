import pytest

from app.services.document_service import load_document


def test_unsupported_document_type():

    with pytest.raises(
        ValueError,
        match="Unsupported file type"
    ):

        load_document(
            "test_file.txt"
        )