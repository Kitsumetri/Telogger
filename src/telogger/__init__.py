from typing import Optional, Union, Type
import logging
import sys
from types import TracebackType
from .client import TelegramClient
from .handlers import TelegramHandler

from .decorators import monitor, monitor_start_stop

class Telogger:
    def __init__(
        self,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        async_mode: bool = False,
    ):
        self.client = TelegramClient(token, chat_id, async_mode)
        self._original_excepthook = sys.excepthook

    def send_message(self, text: str) -> bool:
        return self.client.send_message(text)

    def add_logging_handler(
        self,
        logger: logging.Logger = logging.getLogger(),
        level: int = logging.ERROR
    ) -> None:
        handler = TelegramHandler(self.client.token, self.client.chat_id)
        handler.setLevel(level)
        logger.addHandler(handler)

    def enable_global_exception_hook(self) -> None:
        def exception_hook(
            exc_type: Type[BaseException],
            exc_value: BaseException,
            traceback: Optional[TracebackType]
        ):
            message = f"🚨 Unhandled Exception: {exc_type.__name__}\n{str(exc_value)}"
            if self.client.async_mode:
                import asyncio
                asyncio.run(self.client.send_message_async(message))
            else:
                self.client.send_message(message)
            
            self._original_excepthook(exc_type, exc_value, traceback)

        sys.excepthook = exception_hook

    def disable_global_exception_hook(self) -> None:
        sys.excepthook = self._original_excepthook
