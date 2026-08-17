"""
tests/test_assistant.py — Unit tests for src/assistant.py

Run with:
    pytest tests/test_assistant.py -v

These tests mock the API call itself (no real network request, no real
API key needed) so they run fast and deterministically in CI. What's
under test is our own logic — mode handling, structured-output parsing,
memory, and error handling — not the model's actual output quality.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.assistant import MODES, ask, ask_structured, format_reply


# ==============================================================================
# Fixtures
# ==============================================================================
@pytest.fixture
def fake_memory():
    """A minimal stand-in for the Streamlit session-memory adapter, so
    tests don't depend on Streamlit being running."""

    class _FakeMemory:
        def __init__(self):
            self.messages = []

        def add(self, role, content):
            self.messages.append({"role": role, "content": content})

        def as_messages(self, system_prompt):
            return [{"role": "system", "content": system_prompt}, *self.messages]

    return _FakeMemory()


def _mock_completion(content: str):
    """Builds a fake object shaped like the SDK's chat completion response,
    just deep enough for our code to read `.choices[0].message.content`."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=content))]
    return mock_response


# ==============================================================================
# MODES
# ==============================================================================
def test_modes_contains_expected_keys():
    expected = {"general", "grammar", "explain", "summarize"}
    assert expected.issubset(set(MODES.keys()))


def test_modes_values_are_non_empty_strings():
    for mode_name, prompt in MODES.items():
        assert isinstance(prompt, str)
        assert len(prompt.strip()) > 0, f"Mode '{mode_name}' has an empty prompt"


# ==============================================================================
# ask()
# ==============================================================================
@patch("src.assistant.client")
def test_ask_returns_model_reply(mock_client, fake_memory):
    mock_client.chat.completions.create.return_value = _mock_completion(
        "This is the assistant's reply."
    )

    reply = ask("Hello there", mode="general", memory=fake_memory)

    assert reply == "This is the assistant's reply."


@patch("src.assistant.client")
def test_ask_stores_user_and_assistant_turns_in_memory(mock_client, fake_memory):
    mock_client.chat.completions.create.return_value = _mock_completion("Reply text")

    ask("What is Python?", mode="explain", memory=fake_memory)

    roles = [m["role"] for m in fake_memory.messages]
    assert "user" in roles
    assert "assistant" in roles


@patch("src.assistant.client")
def test_ask_falls_back_to_general_on_unknown_mode(mock_client, fake_memory):
    """An unrecognized mode shouldn't crash — it should behave like
    'general' rather than raising a KeyError deep in the request."""
    mock_client.chat.completions.create.return_value = _mock_completion("ok")

    # Should not raise
    reply = ask("test input", mode="not_a_real_mode", memory=fake_memory)
    assert isinstance(reply, str)


@patch("src.assistant.client")
def test_ask_raises_runtime_error_on_api_failure(mock_client, fake_memory):
    mock_client.chat.completions.create.side_effect = Exception("connection refused")

    with pytest.raises(RuntimeError):
        ask("Hello", mode="general", memory=fake_memory)


# ==============================================================================
# ask_structured()
# ==============================================================================
@patch("src.assistant.client")
def test_ask_structured_returns_parsed_dict(mock_client):
    payload = {
        "title": "Test Title",
        "summary": "A short summary.",
        "keywords": ["one", "two", "three"],
    }
    mock_client.chat.completions.create.return_value = _mock_completion(
        json.dumps(payload)
    )

    result = ask_structured("Some input text to summarize.")

    assert result["title"] == "Test Title"
    assert result["keywords"] == ["one", "two", "three"]


@patch("src.assistant.client")
def test_ask_structured_handles_code_fenced_json(mock_client):
    """Models frequently wrap JSON in ```json fences even when told not
    to — this should still parse correctly."""
    fenced = '```json\n{"title": "T", "summary": "S", "keywords": ["a"]}\n```'
    mock_client.chat.completions.create.return_value = _mock_completion(fenced)

    result = ask_structured("input text")

    assert result["title"] == "T"
    assert result["keywords"] == ["a"]


@patch("src.assistant.client")
def test_ask_structured_raises_value_error_on_invalid_json(mock_client):
    mock_client.chat.completions.create.return_value = _mock_completion(
        "This is not JSON at all."
    )

    with pytest.raises(ValueError):
        ask_structured("input text")


# ==============================================================================
# format_reply()
# ==============================================================================
def test_format_reply_strips_surrounding_whitespace():
    assert format_reply("  hello world  \n") == "hello world"


def test_format_reply_handles_empty_string():
    assert format_reply("") == ""


def test_format_reply_leaves_normal_text_unchanged():
    text = "This is a normal reply with punctuation."
    assert format_reply(text) == text
