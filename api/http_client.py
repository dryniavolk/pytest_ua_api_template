from typing import Any, Protocol
import requests


class CookieProvider(Protocol):
    """Шаблон для работы с cookies"""
    def get_cookies(self) -> dict[str, str]: ...


class AviasalesHttpClient:
    """Выполняет запросы к API, автоматически добавляя cookies и нужные заголовки."""

    DEFAULT_ORIGIN = "https://www.aviasales.ru"
    DEFAULT_REFERER = "https://www.aviasales.ru/"
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def __init__(self, cookie_provider: CookieProvider) -> None:
        self._cookie_provider = cookie_provider

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        cookies = self._cookie_provider.get_cookies()
        cookie_header_value = "; ".join(f"{k}={v}" for k, v in cookies.items())
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "user-agent": self.DEFAULT_USER_AGENT,
            "origin": self.DEFAULT_ORIGIN,
            "referer": self.DEFAULT_REFERER,
            "Cookie": cookie_header_value,
        }
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        kwargs["cookies"] = cookies
        return requests.request(method, url, **kwargs)
