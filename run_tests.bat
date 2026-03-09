@echo off
chcp 65001 >nul
setlocal

rem ==== НАСТРОЙКА ПУТЕЙ ====
set results=.\results
set rep_history=.\final-report\history
set report=.\final-report

echo ==========================================
echo    ЗАПУСК АВТОТЕСТОВ И ГЕНЕРАЦИЯ ОТЧЕТА
echo ==========================================

rem ==== 1. ОЧИСТКА ====
echo [1/5] Очистка старых результатов...
if exist %results% rmdir /s /q %results% 2>nul
echo   ✓ Папка results очищена

rem ==== 2. ТЕСТЫ ====
echo [2/5] Запуск тестов (pytest)...
pytest tests/ --alluredir=%results% -v -s
if errorlevel 1 echo   ⚠ ВНИМАНИЕ: Некоторые тесты упали!

rem ==== 3. ИСТОРИЯ ====
echo [3/5] Копирование истории...
if exist %rep_history% (
    xcopy %rep_history% %results%\history /E /I /Y >nul
    echo   ✓ История скопирована
) else (
    echo   ℹ История не найдена (первый запуск?)
)

rem ==== 4. ГЕНЕРАЦИЯ ====
echo [4/5] Генерация отчета Allure...
if exist %report% rmdir /s /q %report% 2>nul
call allure generate %results% -o %report% --clean
if errorlevel 1 (
    echo   ❌ ОШИБКА: Не удалось сгенерировать отчет. Проверь установку Java/Allure.
    pause
    exit /b 1
)
echo   ✓ Отчет сгенерирован в папку %report%

rem ==== 5. ОТКРЫТИЕ (САМОЕ ВАЖНОЕ) ====
echo [5/5] Открытие отчета в браузере...
echo   🚀 Запуск локального сервера...
echo   ---------------------------------------------------
echo   Если браузер не открылся автоматически, скопируй ссылку:
echo   http://localhost:56789 (порт может отличаться)
echo   ---------------------------------------------------

rem Используем 'call', чтобы скрипт ждал завершения команды allure open
rem Команда 'start' запускает новое окно, которое не убьет основной процесс
start "" allure open %report%

echo.
echo ==========================================
echo ГОТОВО! 
echo Отчет должен открыться в браузере.
echo Черное окно с сервером можно не закрывать, пока смотришь отчет.
echo ==========================================
pause