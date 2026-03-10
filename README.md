# pytest_ui_api_template

## Шаблон для автоматизации тестирования на python

### Шаги
1. Склонировать проект 'https://github.com/dryniavolk/pytest_ua_api_template.git'
2. Установить зависимости
# pip install -r requirements.txt
3. Запуск тестов
# API + UI тесты
bash
Все тесты
pytest

Только UI-тесты
pytest -m ui

Только API-тесты
pytest -m api   

# С генерацией Allure отчёта
pytest tests/ -v --alluredir=allure-results

allure serve allure-results

или сразу .\run_tests.bat он сформирует отчёт в allure-results

### Стек:
- pytest
- selenium
- requests
- allure
- config

### Струткура:
- ./test - тесты
- ./pages - описание страниц
- ./api - хелперы для работы с API

pytest_ua_api_template/
├── api/
│   ├── __init__.py
│   ├── aviasales_api.py          # API клиент Aviasales
│   ├── cookie_manager.py          # Менеджер cookies (Selenium + cache)
│   └── http_client.py             # HTTP клиент с заголовками
├── pages/
│   ├── __init__.py
│   ├── mainPage.py                # Page Object: главная страница
│   └── resultPage.py              # Page Object: страница результатов
├── tests/
│   ├── __init__.py
│   ├── api_test.py                # 5 API тестов
│   └── ui_test.py                 # 5 UI тестов
├── postman/
│   └── Aviasales_10_API_Tests.json # Postman коллекция
├── conftest.py                     # Pytest фикстуры (WebDriver)
├── pytest.ini                      # Настройки pytest
├── requirements.txt                # Зависимости
├── README.md                       # Документация
└── allure-results/                 # Результаты Allure (gitignored)

### Стек:
- pytest
- selenium
- requests
- allure

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [финальная работа по ручному тестированию Aviasales](https://volkavtest.yonote.ru/share/638ff0ef-35e2-48a7-9a52-2bc0af61bbcf)

### Библиотеки для установки
- pyp install pytest
- pip install selenium
- pip install webdriver-manager
- pip install requests
- pip install allure

