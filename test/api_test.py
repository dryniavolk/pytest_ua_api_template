import allure
import pytest
from api.aviasales_api import AviasalesAPI

pytestmark = pytest.mark.api


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("API: Поиск билетов в оба конца")
@allure.story("API-тестирование поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_roundtrip_flight_search() -> None:
    api_client = AviasalesAPI()

    with allure.step("Запустить поиск билетов туда-обратно"):
        search_uid = api_client.search_start(
            origin='IJK',
            destination='MOW',
            date_from='2026-11-08',
            date_to='2026-11-09',
            adults=1
        )
        assert search_uid is not None

    with allure.step("Получить результаты по поиска"):
        search_results = api_client.search_result(search_uid)
        assert search_results is not None


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("API: в одну сторону поиск билетов")
@allure.story("API-тестирование поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_oneway_flight_search() -> None:
    api_client = AviasalesAPI()

    with allure.step("Запустить поиск в один конец"):
        search_uid = api_client.search_one_way(
            origin='IJK',
            destination='MOW',
            date='2026-11-08',
            adults=1
        )
        assert search_uid is not None

    with allure.step("Запросить данные выдачи"):
        search_results = api_client.search_result(search_uid)
        assert search_results is not None


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("API: Длинный диапазон дат")
@allure.story("API-тестирование поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_extended_date_range_search() -> None:
    api_client = AviasalesAPI()

    with allure.step("Запрос с большим разрывом между датами"):
        search_uid = api_client.search_start(
            origin='IJK',
            destination='MOW',
            date_from='2026-11-08',
            date_to='2027-02-08',
            adults=1
        )
        assert search_uid is not None

    with allure.step("Убедиться, что результаты есть"):
        search_results = api_client.search_result(search_uid)
        assert search_results is not None


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("API: Поиск с ребенком в составе пассажиров")
@allure.story("API-тестирование поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_search_with_infant_passenger() -> None:
    api_client = AviasalesAPI()

    with allure.step("Запустить поиск с параметром infant=1"):
        search_uid = api_client.search_start(
            origin='IJK',
            destination='MOW',
            date_from='2026-11-08',
            date_to='2026-11-09',
            adults=1,
            infants=1
        )
        assert search_uid is not None

    with allure.step("Проверить ответ"):
        search_results = api_client.search_result(search_uid)
        assert search_results is not None


@allure.feature("Авиасейлс: поиск и бронирование авиабилетов")
@allure.title("API: города отправления и назначения одинаковы")
@allure.story("API-тестирование поиска")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_invalid_same_origin_destination() -> None:
    api_client = AviasalesAPI()

    with allure.step("ЗапусК поиска с одинаковыми городами"):
        search_uid = api_client.search_start(
            origin='IJK',
            destination='IJK',
            date_from='2026-11-08',
            date_to='2026-11-09',
            adults=1
        )
        assert search_uid is None
