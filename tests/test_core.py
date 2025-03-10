import pytest
from src.telogger import Telogger
import logging
import os

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("TELOGGER_TOKEN", "fake_token")
    monkeypatch.setenv("TELOGGER_CHAT_ID", "12345")

def test_send_message_success(mock_env, httpx_mock):
    # Mock the Telegram API response
    httpx_mock.add_response(
        url="https://api.telegram.org/botfake_token/sendMessage",
        json={"ok": True},
        status_code=200,
    )

    tg = Telogger()
    assert tg.send_message("Test") is True

def test_logging_handler(mock_env, caplog):
    tg = Telogger()
    logger = logging.getLogger("test_logger")
    tg.add_logging_handler(logger, level=logging.INFO)
    
    with caplog.at_level(logging.INFO):
        logger.info("Test log")
    
    assert "Test log" in caplog.text