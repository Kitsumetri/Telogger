import pytest
from src.telogger import Telogger
import sys
import json

def test_exception_hook_sync(mock_env, httpx_mock):
    # Mock the Telegram API response
    httpx_mock.add_response(
        url="https://api.telegram.org/botfake_token/sendMessage",
        json={"ok": True}
    )
    
    tg = Telogger()
    tg.enable_global_exception_hook()

    try:
        raise ValueError("Test error")
    except ValueError:
        sys.excepthook(*sys.exc_info())

    # Get the captured request
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    
    request = requests[0]
    request_data = json.loads(request.content)
    assert "Unhandled Exception" in request_data["text"]