from typing import Any, Protocol
import requests
from config import AVIASALES_MAIN_URL


class CookieProvider(Protocol):
    """Шаблон для работы с cookies."""
    def get_cookies(self) -> dict[str, str]: ...


class AviasalesHttpClient:
    """Выполняет запросы к API, добавляя cookies и заголовки."""

    DEFAULT_ORIGIN = AVIASALES_MAIN_URL
    DEFAULT_REFERER = f"{AVIASALES_MAIN_URL}/"
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36"
    )

    def __init__(self, cookie_provider: CookieProvider) -> None:
        self._cookie_provider = cookie_provider

    def request(
        self,
        method: str,
        url: str,
        **kwargs: Any
    ) -> requests.Response:
        cookies = self._cookie_provider.get_cookies()
        cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": self.DEFAULT_USER_AGENT,
            "origin": self.DEFAULT_ORIGIN,
            "referer": self.DEFAULT_REFERER,
            "Cookie": cookie_header,
        }
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        kwargs["cookies"] = cookies
        return requests.request(method, url, **kwargs)
