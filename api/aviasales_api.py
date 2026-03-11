import time
from typing import Any, Optional

from api.cookie_manager import CookieManager
from api.http_client import AviasalesHttpClient
from config import (
    AVIASALES_API_URL,
    SEARCH_START_ENDPOINT,
    SEARCH_RESULTS_ENDPOINT,
)


class AviasalesAPI:
    """API-клиент для поиска авиабилетов."""

    def __init__(self) -> None:
        cookie_manager = CookieManager()
        self._http_client = AviasalesHttpClient(cookie_manager)
        self.base_url = AVIASALES_API_URL
        self.search_uid: Optional[str] = None
        self.last_request_id: Optional[str] = None

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> Any:
        url = f"{self.base_url}{endpoint}"
        if self.last_request_id:
            headers = kwargs.setdefault("headers", {})
            headers["X-Request-Id"] = self.last_request_id
        response = self._http_client.request(method, url, **kwargs)
        if "X-Request-Id" in response.headers:
            self.last_request_id = response.headers["X-Request-Id"]
        return response

    def search_start(
        self,
        origin: str,
        destination: str,
        date_from: str,
        date_to: str,
        adults: int = 1,
        children: int = 0,
        infants: int = 0,
    ) -> Optional[str]:
        payload = {
            "search_params": {
                "directions": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "date": date_from,
                    },
                    {
                        "origin": destination,
                        "destination": origin,
                        "date": date_to,
                    },
                ],
                "passengers": {
                    "adults": adults,
                    "children": children,
                    "infants": infants,
                },
                "trip_class": "Y",
            },
            "marker": "direct",
            "market_code": "ru",
            "currency_code": "rub",
        }
        response = self._make_request(
            "post",
            SEARCH_START_ENDPOINT,
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            self.search_uid = data.get("search_id")
            return self.search_uid
        return None

    def search_one_way(
        self,
        origin: str,
        destination: str,
        date: str,
        adults: int = 1,
        children: int = 0,
        infants: int = 0,
    ) -> Optional[str]:
        payload = {
            "search_params": {
                "directions": [
                    {
                        "origin": origin,
                        "destination": destination,
                        "date": date,
                    }
                ],
                "passengers": {
                    "adults": adults,
                    "children": children,
                    "infants": infants,
                },
                "trip_class": "Y",
            },
            "marker": "direct",
            "market_code": "ru",
            "currency_code": "rub",
        }
        response = self._make_request(
            "post",
            SEARCH_START_ENDPOINT,
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            self.search_uid = data.get("search_id")
            return self.search_uid
        return None

    def search_result(
        self,
        search_uid: Optional[str] = None
    ) -> Optional[list]:
        if search_uid is not None:
            self.search_uid = search_uid
        if not self.search_uid:
            return None
        
        current_timestamp = int(time.time())
        time.sleep(2)
        
        payload = {
            "limit": 1,
            "price_per_person": False,
            "search_by_airport": False,
            "search_id": self.search_uid,
            "last_update_timestamp": current_timestamp,
        }
        
        for _ in range(5):
            response = self._make_request(
                "post",
                SEARCH_RESULTS_ENDPOINT,
                json=payload
            )
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0 and "tickets" in data[0]:
                    return data
            elif response.status_code in (204, 304):
                time.sleep(2)
                continue
            else:
                return None
        return None
