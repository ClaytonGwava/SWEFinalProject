from unittest.mock import Mock, patch

from app.services.llm_service import ask_llm


def test_ask_llm_returns_ai_response():

    mock_response = Mock()

    mock_response.output_text = (
        "Software engineering is a systematic approach "
        "to developing software."
    )

    with patch(
        "app.services.llm_service.client.responses.create",
        return_value=mock_response
    ) as mock_create:

        result = ask_llm(
            "What is software engineering?",
            "Software engineering is a systematic approach "
            "to software development."
        )

        assert result == (
            "Software engineering is a systematic approach "
            "to developing software."
        )

        mock_create.assert_called_once()


def test_ask_llm_passes_question_and_context():

    mock_response = Mock()

    mock_response.output_text = "Test answer"

    with patch(
        "app.services.llm_service.client.responses.create",
        return_value=mock_response
    ) as mock_create:

        result = ask_llm(
            "What is Agile?",
            "Agile is an iterative software development approach."
        )

        assert result == "Test answer"

        call_arguments = (
            mock_create.call_args.kwargs
        )

        assert call_arguments["model"] == "gpt-5-mini"

        messages = call_arguments["input"]

        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

        assert "What is Agile?" in (
            messages[1]["content"]
        )

        assert "Agile is an iterative" in (
            messages[1]["content"]
        )