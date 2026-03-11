# pytest_ui_api_template

## Автоматизированное тестирования Aviasales


### Стек:
- Pytest
- Selenium
- requests
- allure
- config

### Структура проекта

```
pytest_ua_api_template/
├── api/
│   ├── __init__.py
│   ├── aviasales_api.py          # API  клиент Aviasales
│   ├── cookie_manager.py         # Менеджер cookies 
│   └── http_client.py            # HTTP клиент 
├── pages/
│   ├── __init__.py
│   ├── mainPage.py               # Page Object: главная страница
│   └── resultPage.py             # Page Object: страница результатов
├── tests/
│   ├── __init__.py
│   ├── api_test.py               # 5 API тестов
│   └── ui_test.py                # 5 UI тестов
├── run_tests.bat                 # Скрипт запуска тестов   
├── conftest.py                   # Pytest фикстуры (WebDriver)
├── pytest.ini                    # Настройки pytest
├── requirements.txt              # Зависимости
├── README.md                     # Документация
└── allure-results/               # Результаты Allure (gitignored)
└── allure-report/                # Результаты Allure в виде html (gitignored)
```  

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- Финальный проект по ручному тестированию[Авиасейлс](https://volkavtest.yonote.ru/share/638ff0ef-35e2-48a7-9a52-2bc0af61bbcf)

### Установка и запуск

1. Клонирование репозитория
'''bash
git clone https://github.com/dryniavolk/pytest_ua_api_template.git
cd pytest_ua_api_template

2. Установка зависимостей

```bash
pip install -r requirements.txt
```

3. Запуск тестов
bash
#### Все тесты
pytest

#### Только UI-тесты
pytest -m ui

#### Только API-тесты
pytest -m api

#### С подробным выводом
pytest -v -s

#### запуск тестов и сразу отчета allure фаилом run_tests.bat
.\run_tests.bat (ввести в консоли в папке пректа)



создание отчёта Allure:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```
