import logging
from typing import Dict, Any, Union
from .client import TelegramClient

class TelegramHandler(logging.Handler):
    def __init__(self, token: str, chat_id: Union[int, str]):
        super().__init__()
        self.client = TelegramClient(token, chat_id)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            self.client.send_message(msg)
        except Exception:
            self.handleError(record)