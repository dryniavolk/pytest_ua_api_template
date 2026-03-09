# pytest_ui_api_template

## Шаблон для автоматизации тестирования на python

### Шаги
1. Склонировать проект 'https://github.com/dryniavolk/pytest_ua_api_template.git'
2. Установить зависимости
3. Запустить тесты 'pytest'

### Стек:
- pytest
- selenium
- requests
- _sqlalchemy_
- allure
- config

### Струткура:
- ./test - тесты
- ./pages - описание страниц
- ./api - хелперы для работы с API
- ./db - хелперы для работы с БД

pytest_api_ui_template/
├── api/                          
│   ├── aviasales_api.py          
│   ├── cookie_manager.py         
│   └── http_client.py            
├── pages/                        
│   ├── mainPage.py              
│   └── resultPage.py             
│
├── test/                        
│   ├── test_api.py               
│   └── test_ui.py                
├── conftest.py                   
├── pytest.ini                     
├── requirements.txt               
└── README.md   

### Стек:
- pytest
- selenium
- requests
- allure

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)

### Библиотеки (!)
- pyp install pytest
- pip install selenium
- pip install webdriver-manager
- pip install requests
- pip install allure

