import os

import openai
import pytest

from cybersentry.sdk.agents import set_default_openai_api, set_default_openai_client, set_default_openai_key
from cybersentry.sdk.agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from cybersentry.sdk.agents.models.openai_provider import OpenAIProvider
from cybersentry.sdk.agents.models.openai_responses import OpenAIResponsesModel


import os
cybersentry_model = os.getenv('Cybersentry_MODEL', "qwen2.5:14b")

def test_cc_no_default_key_errors(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(openai.OpenAIError):
        OpenAIProvider(use_responses=False).get_model(cybersentry_model)


def test_cc_set_default_openai_key():
    set_default_openai_key("test_key")
    chat_model = OpenAIProvider(use_responses=False).get_model(cybersentry_model)
    assert chat_model._client.api_key == "test_key"  # type: ignore


def test_cc_set_default_openai_client():
    client = openai.AsyncOpenAI(api_key="test_key")
    set_default_openai_client(client)
    chat_model = OpenAIProvider(use_responses=False).get_model(cybersentry_model)
    assert chat_model._client.api_key == "test_key"  # type: ignore


def test_resp_no_default_key_errors(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert os.getenv("OPENAI_API_KEY") is None
    with pytest.raises(openai.OpenAIError):
        OpenAIProvider(use_responses=True).get_model(cybersentry_model)


def test_resp_set_default_openai_key():
    set_default_openai_key("test_key")
    resp_model = OpenAIProvider(use_responses=True).get_model(cybersentry_model)
    assert resp_model._client.api_key == "test_key"  # type: ignore


def test_resp_set_default_openai_client():
    client = openai.AsyncOpenAI(api_key="test_key")
    set_default_openai_client(client)
    resp_model = OpenAIProvider(use_responses=True).get_model(cybersentry_model)
    assert resp_model._client.api_key == "test_key"  # type: ignore


def test_set_default_openai_api():
    assert isinstance(OpenAIProvider().get_model(cybersentry_model), OpenAIResponsesModel), (
        "Default should be responses"
    )

    set_default_openai_api("chat_completions")
    assert isinstance(OpenAIProvider().get_model(cybersentry_model), OpenAIChatCompletionsModel), (
        "Should be chat completions model"
    )

    set_default_openai_api("responses")
    assert isinstance(OpenAIProvider().get_model(cybersentry_model), OpenAIResponsesModel), (
        "Should be responses model"
    )
