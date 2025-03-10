from typing import Optional, Union
import httpx
import os

class TelegramClient:
    def __init__(
        self,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        async_mode: bool = False
    ):
        self.token = token or os.getenv("TELOGGER_TOKEN")
        self.chat_id = str(chat_id or os.getenv("TELOGGER_CHAT_ID"))
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        self.async_mode = async_mode
        self.client = httpx.AsyncClient() if async_mode else httpx.Client(timeout=10)

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        return self._send_sync(text, parse_mode)

    async def send_message_async(self, text: str, parse_mode: str = "HTML") -> bool:
        return await self._send_async(text, parse_mode)

    def _send_sync(self, text: str, parse_mode: str) -> bool:
        try:
            response = self.client.post(
                self.api_url,
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                }
            )
            response.raise_for_status()
            return True
        except (httpx.HTTPError, ValueError):
            return False

    async def _send_async(self, text: str, parse_mode: str) -> bool:
        try:
            response = await self.client.post(
                self.api_url,
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode
                }
            )
            response.raise_for_status()
            return True
        except (httpx.HTTPError, ValueError):
            return False