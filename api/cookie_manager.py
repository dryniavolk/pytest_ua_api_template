import json
import os
from datetime import datetime, timedelta
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class CookieManager:
    """Кэширование cookies для доступа к Aviasales"""

    def __init__(self, cookie_file: str = "aviasales_cookies.json") -> None:
        self.cookie_file = cookie_file

    def get_cookies(self) -> dict[str, str]:
        cookies = self._load_cookies()
        if cookies is not None:
            return cookies
        cookies = self._get_fresh_cookies()
        self._save_cookies(cookies)
        return cookies

    def _load_cookies(self) -> Optional[dict[str, str]]:
        if not os.path.exists(self.cookie_file):
            return None
        try:
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            expires = datetime.fromisoformat(data["expires"])
            if datetime.now() < expires:
                return data["cookies"]
        except (json.JSONDecodeError, KeyError, ValueError):
            # Если файл повреждён — игнорируем и получаем свежие
            pass
        return None

    def _save_cookies(self, cookies: dict[str, str]) -> None:
        data = {
            "cookies": cookies,
            "expires": (datetime.now() + timedelta(minutes=30)).isoformat(),
        }
        with open(self.cookie_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _get_fresh_cookies(self) -> dict[str, str]:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        try:
            driver.get("https://www.aviasales.ru")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            cookies: dict[str, str] = {}
            for cookie in driver.get_cookies():
                cookies[cookie["name"]] = cookie["value"]
            return cookies
        finally:
            driver.quit()