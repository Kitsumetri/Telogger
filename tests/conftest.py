import pytest
import os

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("TELOGGER_TOKEN", "fake_token")
    monkeypatch.setenv("TELOGGER_CHAT_ID", "12345")