import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.resultPage import ResultPage
from pages.mainPage import MainPage

pytestmark = pytest.mark.ui


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("UI: Поиск билетов в оба конца")
@allure.story("тестирование поиска")
@allure.severity("Critical")
def test_ui_roundtrip_ticket_search(driver: WebDriver) -> None:
    home_page = MainPage(driver)
    results_page = ResultPage(driver)

    with allure.step("Перейти на главную страницу сервиса"):
        home_page.navigate()

    with allure.step("Заполнить параметры: Ижевск → Москва, даты"):
        home_page.fill_departure_city('Ижевск')
        home_page.fill_arrival_city('Москва')
        home_page.select_departure_date('19.03.2026')
        home_page.select_return_date('20.03.2026')

    with allure.step("Запустить поиск"):
        home_page.click_search()

    with allure.step("Дождаться выдачи и проверить цену"):
        results_page.wait_for_prices_loaded(timeout=45)
        ticket_price = results_page.get_ticket_price()
        assert ticket_price, "Цена билета не отображается"
        assert results_page.is_price_valid(ticket_price), f"Некорректный формат цены: '{ticket_price}'"


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("UI: Поиск билетов в одну сторону")
@allure.story("тестирование поиска")
@allure.severity("Critical")
def test_ui_oneway_ticket_search(driver: WebDriver) -> None:
    home_page = MainPage(driver)
    results_page = ResultPage(driver)

    with allure.step("Открыть главную страницу"):
        home_page.navigate()

    with allure.step("Ввести город и дату вылета"):
        home_page.fill_departure_city('Ижевск')
        home_page.fill_arrival_city('Москва')
        home_page.select_departure_date('19.03.2026')

    with allure.step("Запустить поиск"):
        home_page.click_search()

    with allure.step("Проверить наличие цены в результате"):
        results_page.wait_for_prices_loaded(timeout=40)
        ticket_price = results_page.get_ticket_price()
        assert ticket_price, "Цена не найдена"
        assert results_page.is_price_valid(ticket_price), f"Цена не прошла валидацию: '{ticket_price}'"


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("UI: Негативный-тест дублирование городов")
@allure.story("тестирование ошибок")
@allure.severity("Critical")
def test_ui_invalid_same_city_search(driver: WebDriver) -> None:
    home_page = MainPage(driver)
    results_page = ResultPage(driver)

    with allure.step("Перейти на сайт"):
        home_page.navigate()

    with allure.step("Указать один и тот же город в оба поля"):
        home_page.fill_departure_city('Ижевск')
        home_page.fill_arrival_city('Ижевск')
        home_page.select_departure_date('19.03.2026')
        home_page.select_return_date('20.03.2026')

    with allure.step("Выполнить поиск"):
        home_page.click_search()

    with allure.step("Убедиться, что результаты отсутствуют"):
        assert results_page.has_no_results(), "Ожидалось сообщение об отсутствии билетов"


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("UI: Добавление в избранное нужна авторизация")
@allure.story("тестирование авторизации")
@allure.severity("Critical")
def test_ui_favourite_requires_auth(driver: WebDriver) -> None:
    results_page = ResultPage(driver)
    home_page = MainPage(driver)

    with allure.step("Выполнить поиск билета"):
        home_page.navigate()
        home_page.fill_departure_city('Ижевск')
        home_page.fill_arrival_city('Москва')
        home_page.select_departure_date('19.03.2026')
        home_page.select_return_date('20.03.2026')
        home_page.click_search()

    with allure.step("Нажать 'В избранное'"):
        results_page.click_favourite_button()

    with allure.step("Проверить отображение формы "):
        assert results_page.is_login_form_displayed(), "Форма авторизации не появилась"
        login_text = results_page.get_login_form_text()
        assert login_text == "Войти в профиль"


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("UI: Поиск с ребенком в пассажирах")
@allure.story("тестирование поиска")
@allure.severity("Critical")
def test_ui_search_with_infant_passenger(driver: WebDriver) -> None:
    home_page = MainPage(driver)
    results_page = ResultPage(driver)

    with allure.step("Открыть главную страницу"):
        home_page.navigate()

    with allure.step("Заполнить маршрут и даты"):
        home_page.fill_departure_city('Ижевск')
        home_page.fill_arrival_city('Москва')
        home_page.select_departure_date('19.03.2026')
        home_page.select_return_date('20.03.2026')

    with allure.step("Добавить 1 ребенка и проверить значение"):
        infant_count = home_page.add_infant()
        assert infant_count == "1", f"Ожидалось '1', получено: '{infant_count}'"

    with allure.step("Запустить поиск и проверить результат"):
        home_page.click_search()
        results_page.wait_for_prices_loaded(timeout=60)
        ticket_price = results_page.get_ticket_price()
        assert results_page.is_price_valid(ticket_price)
