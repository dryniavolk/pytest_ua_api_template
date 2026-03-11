# config.py
"""Конфигурация проекта — все URL и настройки."""

# Основные URL
AVIASALES_MAIN_URL = "https://www.aviasales.ru"
AVIASALES_API_URL = "https://tickets-api.aviasales.ru"

# Endpoints
SEARCH_START_ENDPOINT = "/search/v2/start"
SEARCH_RESULTS_ENDPOINT = "/search/v3.2/results"

# Таймауты и задержки
SEARCH_RESULT_TIMEOUT = 45
API_RETRY_COUNT = 5
API_RETRY_DELAY = 2

# Файлы
COOKIE_FILE = "aviasales_cookies.json"
COOKIE_EXPIRE_MINUTES = 30
